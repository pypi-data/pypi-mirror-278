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
"""Module for define CLI"""
from __future__ import annotations

import argparse
import base64
import logging
import os
import pathlib
from base64 import binascii  # type: ignore

import cryptography.hazmat.primitives.serialization
import platformdirs

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.consts import (
    CONNECTION_FILE_PLACEHOLDER,
    KERNEL_MIN_PORTS_REQUIRED,
    MAX_PORT,
)
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.ip_tools import GetIPException, get_ip, is_valid_hostname

# pylint: disable=too-few-public-methods


def positive_float(value: str) -> float:
    """Make sure that given string is positive flowt"""
    try:
        f_value = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is invalid float value") from exc
    if f_value <= 0:
        raise argparse.ArgumentTypeError(f"{value!r} is not a positive float")
    return f_value


def positive_int(value: str) -> int:
    """Make sure that given string is positive integer"""
    try:
        f_value = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is invalid int value") from exc
    if f_value <= 0:
        raise argparse.ArgumentTypeError(f"{value!r} is not a positive int")
    return f_value


class KernelStarterCLI:
    """Main class"""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--log-level",
            type=self._check_log_level,
            dest="log_level",
            metavar="<log_level>",
            default=os.getenv("JKS_LOG_LEVEL", "INFO"),
            # fmt: off
            help=(
                "Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). "
                "Can be specified as JKS_LOG_LEVEL environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--kernel-id",
            dest="kernel_id",
            metavar="<kernel_id>",
            default=os.getenv("JKS_KERNEL_ID"),
            help="ID of the Jupyter kernel",
        )
        self.parser.add_argument(
            "--response-address",
            dest="response_address",
            metavar="<ip>:<port>",
            default=os.getenv("JKS_RESPONSE_ADDRESS"),
            # fmt: off
            help=(
                "Address of the server to return kernel connection info. "
                "Can be specified as JKS_RESPONSE_ADDRESS environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--bind-ip",
            dest="bind_ip",
            metavar="<x.x.x.x>",
            default=os.getenv("JKS_BIND_IP"),
            # fmt: off
            help=(
                "IP address to bind. "
                "Can be specified as JKS_BIND_IP environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--bind-network",
            metavar="<x.x.x.x/y>",
            default=os.getenv("JKS_BIND_NETWORK"),
            # fmt: off
            help=(
                "Alternatively IP network to bind. "
                "Can be specified as JKS_BIND_NETWORK environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--port-range",
            dest="port_range",
            metavar="<begin>..<end>",
            default=os.getenv("JKS_PORT_RANGE", "1024..65535"),
            # fmt: off
            help=(
                "Range of the ports to use for kernel. "
                "Can be specified as JKS_PORT_RANGE environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--port-bind-attempts",
            dest="port_bind_attempts",
            type=positive_int,
            metavar="<n>",
            default=os.getenv("JKS_PORT_BIND_ATTEMPTS", "5"),
            # fmt: off
            help=(
                "How many times to try to find unoccupied ports to use. "
                "Can be specified as JKS_PORT_BIND_ATTEMPTS environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--wait-ports-timeout",
            dest="wait_ports_timeout",
            type=positive_float,
            metavar="<sec>",
            default=os.getenv("JKS_WAIT_PORTS_TIMEOUT", "10"),
            # fmt: off
            help=(
                "How many seconds wait kernel to open ports before sending connection information to the server. "
                "Can be specified as JKS_WAIT_PORTS_TIMEOUT environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--shutdown-timeout",
            dest="shutdown_timeout",
            type=positive_float,
            metavar="<sec>",
            default=os.getenv("JKS_SHUTDOWN_TIMEOUT", "15"),
            # fmt: off
            help=(
                "Timeout to shutdown kernel if connection to server is lost. "
                "Can be specified as JKS_SHUTDOWN_TIMEOUT environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--response-server-socket-timeout",
            dest="response_server_socket_timeout",
            type=positive_float,
            metavar="<sec>",
            default=os.getenv("JKS_RESPONSE_SERVER_SOCKET_TIMEOUT", "5"),
            # fmt: off
            help=(
                "Socket timeout value for connecting to response server. "
                "Can be specified as JKS_RESPONSE_SERVER_SOCKET_TIMEOUT environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--watchdog-interval",
            dest="watchdog_interval",
            type=positive_float,
            metavar="<sec>",
            default=os.getenv("JKS_WATCHDOG_INTERVAL", "3"),
            # fmt: off
            help=(
                "How often watchdog with check liveness of kernel and connection to server. "
                "Can be specified as JKS_WATCHDOG_INTERVAL environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--kernel-script",
            dest="kernel_script",
            metavar="<cmd>",
            default=os.getenv("JKS_KERNEL_SCRIPT"),
            # fmt: off
            help=(
                f"Script to run; {CONNECTION_FILE_PLACEHOLDER!r} placeholder will be substituted. "
                "Can be specified as JKS_KERNEL_SCRIPT environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--kernel-script-base64",
            dest="kernel_script_base64",
            metavar="<cmd_base64>",
            default=os.getenv("JKS_KERNEL_SCRIPT_BASE64"),
            # fmt: off
            help=(
                "Alternatively cmd can be in base64 format to avoid issues with templating. "
                "Can be specified as JKS_KERNEL_SCRIPT_BASE64 environment variable."
            ),
            # fmt: on
        )
        self.parser.add_argument(
            "--connection-file-dir",
            dest="connection_file_dir",
            metavar="<path>",
            default=os.getenv("JKS_CONNECTION_FILE_DIR", platformdirs.user_data_dir("jupyter", appauthor=False)),
            help="Directory to store connection file json",
        )
        self.parser.add_argument(
            "--encryption-key",
            dest="encryption_key",
            metavar="<pem_key>",
            default=os.getenv("JKS_ENCRYPTION_KEY"),
            # fmt: off
            help=(
                "Public key to encrypt data; must be in string in PEM format or path to .pem file. "
                "Can be specified as JKS_ENCRYPTION_KEY environment variable"
            ),
            # fmt: on
        )

    def _check_log_level(self, value: str) -> str:
        log_level = value.upper()
        if log_level not in logging._nameToLevel:  # pylint: disable=protected-access
            raise argparse.ArgumentTypeError(
                f"Invalid log level: {value}. Choose from DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        return log_level

    def _check_kernel_id(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --bind-ip and --bind-network"""
        if not args:
            return None
        if not args.kernel_id:
            self.parser.error("'--kernel-id' must be provided")
            return None
        return args

    # pylint: disable=too-many-return-statements

    def _check_response_address(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --response-address"""
        if not args:
            return None
        if not args.response_address:
            self.parser.error("'--response-address' must be provided")
            return None
        try:
            listening_ip, listening_port = args.response_address.split(":")
        except ValueError:
            self.parser.error(f"'--response-address' must be in format '<ip>:<port>'. Got {args.response_address!r}")
            return None
        try:
            listening_port = int(listening_port)
        except ValueError:
            self.parser.error(f"Port for '--response-address' must be integer'. Got {listening_port!r}")
            return None
        if not 0 < listening_port < MAX_PORT:
            self.parser.error(f"Port for '--response-address' must be in [0..{MAX_PORT}]'. Got {listening_port!r}")
            return None
        if not is_valid_hostname(listening_ip):
            self.parser.error(f"Host for '--response-address' must be a valid hostname or IP '. Got {listening_ip!r}")
            return None
        args.response_address = listening_ip, listening_port
        return args

    def _check_port_range(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --port-range"""
        if not args:
            return None
        if not args.port_range:
            self.parser.error("'--port-range' must be specified")
            return None
        try:
            begin_port, end_port = map(int, args.port_range.split(".."))
        except ValueError:
            self.parser.error(
                f"Unable to parse provided '--port-range'. Must be in format <begin>..<end>. Got {args.port_range!r}"
            )
            return None
        if begin_port == 0 and end_port == 0:
            args.port_range = 1024, MAX_PORT
            return args
        if not 0 < begin_port < MAX_PORT:
            self.parser.error(f"Begin port must be in [0..{MAX_PORT}]")
            return None
        if not 0 < end_port < MAX_PORT:
            self.parser.error(f"End port should be in [0..{MAX_PORT}]")
            return None
        port_range = end_port - begin_port
        if port_range < KERNEL_MIN_PORTS_REQUIRED:
            self.parser.error(f"'--port-range' should include at least {KERNEL_MIN_PORTS_REQUIRED} ports")
            return None
        args.port_range = begin_port, end_port
        return args

    # pylint: enable=too-many-return-statements

    def _check_kernel_script(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --kernel-script and --kernel-script-base64"""
        if not args:
            return None
        if not (args.kernel_script or args.kernel_script_base64):
            self.parser.error("'--kernel-script' or '--kernel-script-base64' must be specified")
            return None
        if args.kernel_script and args.kernel_script_base64:
            self.parser.error("Only '--kernel-script' or '--kernel-script-base64' must be specified")
            return None
        if args.kernel_script_base64:
            try:
                args.kernel_script = base64.b64decode(args.kernel_script_base64.encode()).decode()
            except binascii.Error as exc:
                self.parser.error(f"Unable to parse {args.kernel_script_base64!r}: {exc!r}")
                return None
        return args

    def _check_encryption_key(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --encryption-key"""
        if not args:
            return None
        if not args.encryption_key:
            self.parser.error("--encryption-key must be specified")
            return None
        encryption_key = pathlib.Path(args.encryption_key)
        try:
            is_file = encryption_key.is_file()
        except OSError:
            is_file = False
        if is_file:
            try:
                with encryption_key.open("rb") as encryption_key_fd:
                    args.encryption_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(
                        encryption_key_fd.read()
                    )
            except IOError as exc:
                self.parser.error(f"Unable to open {args.encryption_key!r}: {exc!r}")
                return None
        else:
            try:
                args.encryption_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(
                    args.encryption_key.encode("utf-8")
                )
            except ValueError as exc:
                self.parser.error(f"Unable to import {args.encryption_key!r} as a valid key: {exc!r}")
                return None
        return args

    def _check_shutdown_timeout(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --shutdown-timeout"""
        if not args:
            return None
        try:
            args.shutdown_timeout = int(args.shutdown_timeout)
        except ValueError:
            self.parser.error(f"--shutdown-timeout should be int: {args.shutdown_timeout!r}")
            return None
        return args

    def _check_bind_ip(self, args: argparse.Namespace | None) -> argparse.Namespace | None:
        """Validate provided input for --bind-ip and --bind-network"""
        if not args:
            return None
        if args.bind_ip and not is_valid_hostname(args.bind_ip):
            self.parser.error(f"--bind-ip must be a valid hostname: {args.bind_ip!r}")
            return None
        try:
            bind_ip = get_ip(args.bind_ip, args.bind_network)
        except GetIPException as exc:
            self.parser.error(f"Unable to find bind IP: {str(exc)!r}")
        args.bind_ip = bind_ip
        return args

    def parse_args(self) -> argparse.Namespace | None:
        """Parse CLI arguments"""
        args = self.parser.parse_args()
        args = self._check_kernel_id(args)
        args = self._check_bind_ip(args)
        args = self._check_shutdown_timeout(args)
        args = self._check_port_range(args)
        args = self._check_response_address(args)
        args = self._check_bind_ip(args)
        args = self._check_kernel_script(args)
        args = self._check_encryption_key(args)
        return args
