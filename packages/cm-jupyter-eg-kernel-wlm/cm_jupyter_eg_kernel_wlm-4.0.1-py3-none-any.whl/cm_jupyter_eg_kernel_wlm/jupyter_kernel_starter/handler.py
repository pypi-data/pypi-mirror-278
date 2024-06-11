#
# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES.
# All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#
"""Module for handle connections to JupyterLab and back"""
from __future__ import annotations

import atexit
import datetime
import json
import logging
import queue
import signal
import socket
import sys
import threading
import time

from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.conn_file import KernelConnectionInfo
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.consts import (
    HANDLER_DATA_BUFF_SIZE,
    HANDLER_QUEUE_SIZE,
    HANDLER_SOCKET_BACKLOG_LEN,
)
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.encryptor import EncryptedMessage, EncryptorDecryptor
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.process_starter import KernelStarter

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes,too-many-arguments


class Handler:
    """Handle connections from server using multithreading
    One thread is a watchdog - monitors if wea re receiving heartbeats from the server
    Another one is poping messages from queue and send signals to the kernel
    Others shortlived (usually a single one at any given time) - receive messaged from the server
        and put them in the queue
    """

    def __init__(
        self,
        response_address: tuple[str, int],
        bind_ip: str,
        socket_timeout: int,
        server_public_key: PublicKeyTypes,
        conn_data: KernelConnectionInfo,
        kernel: KernelStarter,
        handler_timeout: int,
        watchdog_interval: int,
    ) -> None:
        self.bind_ip = bind_ip
        self.socket_timeout = socket_timeout
        self.conn_data = conn_data
        self.bind_port = conn_data.comm_port
        self.response_address = response_address
        self.encryptor = EncryptorDecryptor(server_public_key)
        # kernel object
        self.kernel = kernel
        self.kernel_exists = True
        self.timeout = datetime.timedelta(seconds=handler_timeout)
        # listening socket for incoming connections
        self.socket: socket.socket | None = None
        # queue to store messages from the server (signals)
        self.message_queue: queue.Queue[str] = queue.Queue(maxsize=HANDLER_QUEUE_SIZE)
        self.dequeue_thread: threading.Thread | None = None
        self.started = False
        # set initial timestamp and start watchdog
        self.watchdog_interval = watchdog_interval
        self.watchdog_timestamp = datetime.datetime.now()
        self.watchdog_thread = threading.Thread(target=self.watchdog)
        self.watchdog_thread.daemon = True
        self.watchdog_thread.start()
        atexit.register(self.cleanup)

    def watchdog(self):
        """Monitor if we are receiving messages from the server. Shutdown everything on timeout"""
        while self.kernel_exists:
            time.sleep(self.watchdog_interval)
            now = datetime.datetime.now()
            if now - self.watchdog_timestamp > self.timeout:
                logger.error("No messages from server in %d seconds. Exiting.", self.timeout.seconds)
                self.cleanup()
                self.kernel.send_signal(signal.SIGKILL)
                return

    def init(self):
        """Initialize the server"""
        if self.socket:
            return
        # create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind socket
        try:
            sock.bind((self.bind_ip, self.conn_data.comm_port))
            sock.listen(HANDLER_SOCKET_BACKLOG_LEN)
        except socket.error as exc:
            sock.close()
            logger.error("Unable to start server on %s:%d: %s", self.bind_ip, self.bind_port, str(exc))
            return
        self.socket = sock
        # start thread to handle messages in the queue
        if self.dequeue_thread:
            return
        self.dequeue_thread = threading.Thread(target=self.dequeue)
        self.dequeue_thread.daemon = True
        self.dequeue_thread.start()

    def dequeue(self):
        """Dequeue messages and send them to kernel"""
        while self.kernel_exists:
            try:
                # wait for a message from the queue
                message = self.message_queue.get(timeout=1)
                if message:
                    self.send_message_to_kernel(message)
            except queue.Empty:
                continue

    def send_message_to_kernel(self, message):
        """Forward message to the kernel"""
        try:
            msg = json.loads(message)
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error("Error decoding message from server: %s", str(exc))
            return
        # try to read signum from the message
        if "shutdown" in msg:
            logger.info("Got 'shutdown' from the server. Exiting.")
            self.cleanup()
            self.kernel.send_signal(signal.SIGKILL)
            sys.exit(9)
        if "signum" in msg:
            try:
                signum = int(msg["signum"])
            except ValueError:
                logger.error("Unknown signal received: %s", str(msg["signum"]))
                return
            kernel_exists = self.kernel.send_signal(signum)
            if not kernel_exists:
                logger.error("Kernel process does not exist")
            # we successfully sent message to the kernel
            self.kernel_exists = kernel_exists
            # update timestamp
            self.watchdog_timestamp = datetime.datetime.now()
        else:
            logger.error("Received unknown message: %s", message)

    def run(self) -> None:
        """Start server"""
        if self.started:
            logger.error("Server already started on %s:%d", self.bind_ip, self.bind_port)
            return
        if not self.socket:
            self.init()
        if not self.socket:
            logger.error("Unable to initialize the socket")
            return
        if not self.send_connection_data():
            logger.error("Unable to send connection info to the server")
            sys.exit(130)
        try:
            while self.kernel_exists:
                message_socket, addr = self.socket.accept()
                logger.debug("Accepted connection from %s", addr)
                # handle new connection in another thread
                message_thread = threading.Thread(target=self.handle_connection, args=(message_socket, addr))
                message_thread.daemon = True
                message_thread.start()
        except socket.error as exc:
            logger.error("Listening socket error: %s", str(exc))
        except KeyboardInterrupt:
            logger.info("Shutting down handler")
        finally:
            self.socket.close()
            logger.info("Stopped listening for server messages")

    def cleanup(self):
        """Cleanup"""
        self.kernel_exists = False
        if self.socket:
            self.socket.close()

    def handle_connection(self, conn_socket: socket.socket, addr: str):
        """Handle messages from server"""
        if not self.kernel_exists:
            logger.debug("Unable to handle connection kernel is stopped")
            conn_socket.close()
            return
        conn_socket.settimeout(self.socket_timeout)
        try:
            received_data = b""
            while True:
                data = conn_socket.recv(HANDLER_DATA_BUFF_SIZE)
                if not data:
                    if received_data:
                        decrypted_data = self.decrypt_message(received_data.decode())
                        if not decrypted_data:
                            logger.error("Unable to decrypt message from the server")
                            break
                        self.message_queue.put(decrypted_data)
                        received_data = b""
                    break
                received_data += data
                if len(received_data) >= HANDLER_DATA_BUFF_SIZE * 1024:
                    logger.error("Message is too long. Unable to handle it")
                    break
        except socket.timeout:
            logger.error("Connection timed out for %s:%d", addr[0], addr[1])
        except socket.error as exc:
            logger.error("Socket error: %s", str(exc))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Could be en exception from cryptography library
            logger.error("Unable to handle message from server: %s", str(exc))
        finally:
            conn_socket.close()
            logger.debug("Connection with %s closed.", addr)

    def send_connection_data(self) -> bool:
        """Send connection data to server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                conn_data_encrypted = self.encryptor.encrypt_connection_info(self.conn_data)
                sock.settimeout(self.socket_timeout)
                sock.connect(self.response_address)
                sock.sendall(json.dumps(conn_data_encrypted._asdict()).encode("utf-8"))
        except socket.timeout:
            logger.error("Connection timed out for %s", str(self.response_address))
            return False
        except socket.error as exc:
            logger.error("Socket error: %s", str(exc))
            return False
        return True

    def decrypt_message(self, message: str) -> str | None:
        """Decrypt message from server"""
        if not message:
            return None
        try:
            message_json = json.loads(message)
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error("The encrypted message from the server is not a valid JSON: '%s'", message)
            logger.error(str(exc))
            return None
        iv = message_json.get("iv")
        msg = message_json.get("msg")
        if not iv:
            logger.error("IV is not defined in the message: '%s'", message)
            return None
        if not msg:
            logger.error("Msg is not defined in the message: '%s'", message)
            return None
        return self.encryptor.message_decrypt(EncryptedMessage(iv=str(iv), msg=str(msg)))
