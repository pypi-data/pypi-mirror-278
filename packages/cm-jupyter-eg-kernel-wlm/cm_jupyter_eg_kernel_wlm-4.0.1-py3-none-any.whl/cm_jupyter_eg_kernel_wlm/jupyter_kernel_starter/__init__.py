# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES.
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
"""Main module"""

import logging
import sys

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.cli import KernelStarterCLI
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.conn_file import KernelConnectionFile, PortsConfiguration
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.handler import Handler
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.process_starter import KernelStarter

# Clear any existing log handlers
for log_handler in logging.root.handlers[:]:
    logging.root.removeHandler(log_handler)

logging.basicConfig(level=logging.INFO, format="[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Main call"""

    cli = KernelStarterCLI()
    args = cli.parse_args()

    logger.setLevel(logging._nameToLevel[args.log_level])  # pylint: disable=protected-access
    logger.info("Bind IP is %s", args.bind_ip)

    kernel_port_confg = PortsConfiguration(
        ip=args.bind_ip,
        begin_port_range=args.port_range[0],
        end_port_range=args.port_range[1],
        port_attempts=args.port_bind_attempts,
    )

    logger.info("Create connection file")
    kcf = KernelConnectionFile(
        port_config=kernel_port_confg,
        connection_file_dir=args.connection_file_dir,
        kernel_id=args.kernel_id,
    )
    kcf.get_connection_info(write_file=True)

    logger.info("Start kernel")
    kernel = KernelStarter(
        kernel_cmd=args.kernel_script,
        kernel_connection_info=kcf.kernel_connection_info,
        kernel_connection_file_path=kcf.connection_file_path,
    )
    pid = kernel.start(
        wait_ports=args.wait_ports_timeout > 0,
        wait_ports_timeout=args.wait_ports_timeout,
        watchdog_interval=args.watchdog_interval,
    )
    if not pid:
        sys.exit(100)

    logger.info("Starting handler")
    handler = Handler(
        response_address=args.response_address,
        bind_ip=args.bind_ip,
        socket_timeout=args.response_server_socket_timeout,
        server_public_key=args.encryption_key,
        conn_data=kcf.kernel_connection_info,
        kernel=kernel,
        handler_timeout=args.shutdown_timeout,
        watchdog_interval=args.watchdog_interval,
    )
    handler.run()
    kernel.watchdog.stop()
