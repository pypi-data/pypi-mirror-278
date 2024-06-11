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
"""Module for starting kernels's process"""
from __future__ import annotations

import atexit
import concurrent.futures
import logging
import os
import pathlib
import shlex
import signal
import socket
import subprocess
import threading
import time

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.conn_file import KernelConnectionInfo
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.consts import CONNECTION_FILE_PLACEHOLDER

logger = logging.getLogger(__name__)


class KernelWatchdog(threading.Thread):
    """Shutdown our own process in kernel is disappear"""

    def __init__(self, pid: int, kernel_connection_file_path: pathlib.Path | None = None, watchdog_interval: int = 1):
        super().__init__()
        self.pid = pid
        self.kernel_connection_file_path = kernel_connection_file_path
        self.watchdog_interval = watchdog_interval
        self.daemon = True
        self._running = True

    def run(self):
        """Monitor if kernel process exist and shutdown our own process on kernel exit"""
        while self.is_process_running(self.pid) and self._running:
            time.sleep(self.watchdog_interval)
        if self._running:
            logger.error("Kernel PID %d has stopped. Shutting down.", self.pid)
            self.remove_connection_file()
            os.kill(os.getpid(), signal.SIGINT)
            time.sleep(self.watchdog_interval * 3)
            logger.error("Forced stop monitoring process")
            os.kill(os.getpid(), signal.SIGTERM)  # last resort

    def stop(self):
        """Stop watchdog"""
        self._running = False
        self.remove_connection_file()

    def remove_connection_file(self) -> None:
        """Remove connection file"""
        if self.kernel_connection_file_path:
            logger.debug("Removing connection file %s", self.kernel_connection_file_path)
            self.kernel_connection_file_path.unlink(missing_ok=True)

    @staticmethod
    def is_process_running(pid):
        """Check if there is a running process with the given PID."""
        logger.debug("Checking if %d still running", pid)
        try:
            pid, status = os.waitpid(pid, os.WNOHANG)
            if pid:
                if os.WIFEXITED(status):
                    logger.error("PID %d exited with exit status %d.", pid, os.WEXITSTATUS(status))
                    return False
                if os.WIFSIGNALED(status):
                    logger.error("PID %d is terminated by signal %d.", pid, os.WTERMSIG(status))
                    return False
                if os.WIFSTOPPED(status):
                    logger.error("PID %d is stopped by signal %d.", pid, os.WSTOPSIG(status))
                    return False
                logger.error("PID %d is exited with unknown status %s", pid, status)
                return False
        except OSError:
            logger.error("PID %d is not running", pid)
            return False
        return True


class KernelStarter:
    """Start kernel"""

    def __init__(
        self,
        kernel_cmd: str,
        kernel_connection_info: KernelConnectionInfo,
        kernel_connection_file_path: pathlib.Path,
    ) -> None:
        self.kernel_cmd = kernel_cmd
        self.kernel_connection_info = kernel_connection_info
        self.kernel_connection_file_path = kernel_connection_file_path
        self.proc: subprocess.Popen | None = None
        atexit.register(self.kill)
        self.watchdog: KernelWatchdog | None = None
        self._wait_for_open_ports = True

    def start(
        self,
        wait_ports: bool = True,
        wait_ports_timeout: int = 10,
        start_watchdog: bool = True,
        watchdog_interval: int = 1,
    ) -> int:
        """Start kernel and return pid"""
        kernel_connection_file_path = self.kernel_connection_file_path.as_posix()
        cmd = shlex.split(
            self.kernel_cmd.replace(
                CONNECTION_FILE_PLACEHOLDER,
                kernel_connection_file_path,
            )
        )
        # we need stdout and stderr to be attached to the current console
        logger.info("Starting kernel:\n%s", cmd)
        proc = subprocess.Popen(cmd)  # pylint: disable=consider-using-with
        self.proc = proc
        logger.info("Started kernel process with PID %d", self.proc.pid)
        if start_watchdog:
            logger.info("Starting watchdog for PID %d", self.proc.pid)
            self.watchdog = KernelWatchdog(
                self.proc.pid,
                kernel_connection_file_path=self.kernel_connection_file_path,
                watchdog_interval=watchdog_interval,
            )
            self.watchdog.start()
        if wait_ports:
            if not self.wait_ports(timeout=wait_ports_timeout, socket_timeout=1):
                return 0
        return self.proc.pid

    @classmethod
    def port_is_open(cls, ip: str, port: int, socket_timeout: int) -> bool:
        """Checks if port open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(socket_timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            logger.info("Port %d is listening", port)
        return result == 0

    def wait_ports(self, timeout, socket_timeout) -> bool:
        """Waits for ports to be open"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._wait_ports, socket_timeout)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                self._wait_for_open_ports = False
                logger.error("Not all ports are listening")
                return False
            except KeyboardInterrupt:
                logger.error("Stopping")
                return False
            finally:
                self._wait_for_open_ports = False
                future.cancel()
                executor.shutdown(wait=False)

    def _wait_ports(self, socket_timeout) -> bool:
        """Wait until ports fromself.kernel_connection_info are listening
        We are checking hb, control and shell ports, as per
        https://jupyter-client.readthedocs.io/en/latest/kernels.html
        """
        ports = {
            self.kernel_connection_info.control_port,
            self.kernel_connection_info.shell_port,
            self.kernel_connection_info.hb_port,
        }
        open_ports: set[int] = set()
        logger.info("Monitor open ports %s", str(ports))
        self._wait_for_open_ports = True
        while self._wait_for_open_ports:
            for port in ports - open_ports:
                if self.port_is_open(self.kernel_connection_info.ip, port, socket_timeout):
                    open_ports.add(port)
                    break
            time.sleep(socket_timeout)
            if not ports - open_ports:
                break
        else:
            return False
        logger.info("All ports are listening")
        return True

    def kill(self) -> None:
        """Forcebly kill the process"""
        if not self.proc:
            return
        logger.info("Killing %d", self.proc.pid)
        try:
            os.kill(self.proc.pid, 9)  # SIGKILL
        except OSError:
            pass
        self._process_cleanup()

    def _process_cleanup(self) -> None:
        """Internal cleanup"""
        if self.proc:
            self.proc.wait(timeout=1)  # timeout should not be needed, but just in case
        self.proc = None

    @property
    def kernel_exists(self) -> bool:
        """Checks if kernel process exists"""
        if self.proc and self.proc.poll() is None:
            return True
        self._process_cleanup()
        return False

    def send_signal(self, signum: int) -> bool:
        """Sends signal. Returns True if kernel exists"""
        if not (self.proc and self.kernel_exists):
            return False
        if signum == 0:
            return True
        logger.info("Received signal %d from the server", signum)
        try:
            os.kill(self.proc.pid, signum)
        except OSError:
            self._process_cleanup()
            return False
        return True
