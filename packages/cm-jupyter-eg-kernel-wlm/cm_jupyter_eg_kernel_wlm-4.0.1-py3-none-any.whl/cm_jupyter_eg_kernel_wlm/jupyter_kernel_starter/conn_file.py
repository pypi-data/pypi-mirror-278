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
"""Module for dealing with connection file"""
from __future__ import annotations

import errno
import json
import logging
import os
import pathlib
import random
import socket
import typing
from binascii import b2a_hex

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.consts import (
    KERNEL_HMAC_KEY_LEN,
    KERNEL_SIGNATURE_SCHEME,
    KERNEL_TRANSPORT,
)

logger = logging.getLogger(__name__)


class ConnectionFileException(RuntimeError):
    """Exception occurred while working with ConnectionFile"""


class KernelConnectionInfo(typing.NamedTuple):
    """Type to define connection info"""

    control_port: int
    shell_port: int
    iopub_port: int
    stdin_port: int
    hb_port: int
    comm_port: int
    ip: str
    key: str
    transport: str
    signature_scheme: str
    kernel_name: str
    kernel_id: str


class PortsConfiguration(typing.NamedTuple):
    """Define port and ip configuration of the kernel"""

    ip: str
    begin_port_range: int
    end_port_range: int
    port_attempts: int


def get_port(port_config: PortsConfiguration) -> int:
    """Try to acquire random port"""
    for _ in range(port_config.port_attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        random_port = random.randint(port_config.begin_port_range, port_config.end_port_range)
        try:
            sock.bind((port_config.ip, random_port))
            return random_port
        except OSError:
            pass
        finally:
            sock.close()
    raise ConnectionFileException(
        f"Unable to find free port in {port_config.begin_port_range}..{port_config.end_port_range} range "
        f"on {port_config.ip} in {port_config.port_attempts} attempts"
    )


def generate_key(lenght: int) -> str:
    """Generate random hey for signing kernel messages"""
    buf = os.urandom(lenght)
    return "-".join(b2a_hex(x).decode("ascii") for x in (buf[:4], buf[4:]))


class KernelConnectionFile:
    """Class to work with connection file"""

    def __init__(
        self,
        port_config: PortsConfiguration,
        connection_file_dir: str,
        kernel_id: str,
    ) -> None:
        self.port_config = port_config
        self._kernel_connection_info: KernelConnectionInfo | None = None
        self.key = generate_key(KERNEL_HMAC_KEY_LEN)
        self.connection_file_dir = connection_file_dir
        self._connection_file_path: pathlib.Path | None = None
        self.kernel_id = kernel_id
        self.kernel_name = kernel_id

    @property
    def kernel_connection_info(self) -> KernelConnectionInfo | None:
        """Returns connection info"""
        return self._kernel_connection_info

    @property
    def connection_file_path(self) -> pathlib.Path | None:
        """Returns path to connection file"""
        return self._connection_file_path

    def get_connection_info(self, write_file: bool = True) -> KernelConnectionInfo:
        """Render connection info"""
        shell_port = get_port(self.port_config)
        control_port = get_port(self.port_config)
        iopub_port = get_port(self.port_config)
        stdin_port = get_port(self.port_config)
        hb_port = get_port(self.port_config)
        comm_port = get_port(self.port_config)
        kernel_connection_info = KernelConnectionInfo(
            control_port=control_port,
            shell_port=shell_port,
            iopub_port=iopub_port,
            stdin_port=stdin_port,
            hb_port=hb_port,
            comm_port=comm_port,
            ip=self.port_config.ip,
            key=self.key,
            transport=KERNEL_TRANSPORT,
            signature_scheme=KERNEL_SIGNATURE_SCHEME,
            kernel_id=self.kernel_id,
            kernel_name=self.kernel_name,
        )
        self._kernel_connection_info = kernel_connection_info
        if write_file:
            self.write_connection_info_file()
        return self._kernel_connection_info

    def write_connection_info_file(self):
        """write connection file to disk"""
        if not self._kernel_connection_info:
            raise ConnectionFileException("Unable to write connection file to disk. Connection info is undefined.")
        dirname = pathlib.Path(self.connection_file_dir)
        if dirname.exists() and not dirname.is_dir():
            raise ConnectionFileException(f"Path exists with the same name as the directory {dirname!r}.")
        try:
            dirname.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise ConnectionFileException(f"Permission denied: unable to create directory {dirname!r}.") from None
        except OSError as error:
            raise ConnectionFileException(f"OS error: {error}") from None

        fname = dirname / f"{self.kernel_id}-kernel.json"

        try:
            fname.touch(mode=0o600, exist_ok=False)
            with fname.open(mode="w", encoding="utf-8") as conn_file_fd:
                conn_file_fd.write(json.dumps(self._kernel_connection_info._asdict(), indent=4))
        except FileExistsError:
            raise ConnectionFileException(f"The file {fname} already exists.") from None
        except IOError as exc:
            if exc.errno == errno.ENOSPC:  # errno 28 is 'No space left on device'
                raise ConnectionFileException("Failed to write file due to insufficient disk space.") from None
            raise ConnectionFileException(f"Failed to write file due to IO error: {exc}") from None

        self._connection_file_path = fname
