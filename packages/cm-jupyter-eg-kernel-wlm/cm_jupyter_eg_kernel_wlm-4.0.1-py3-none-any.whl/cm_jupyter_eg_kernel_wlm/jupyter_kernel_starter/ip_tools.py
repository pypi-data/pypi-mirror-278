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
"""Helper module to calculate IPs"""
from __future__ import annotations

import ipaddress
import re
import socket
import typing

import psutil

if typing.TYPE_CHECKING:
    from collections.abc import Sequence


class GetIPException(RuntimeError):
    """Exception occurred while calculating IPs"""


def is_valid_hostname(hostname: str) -> bool:
    """Check if given hostname is a valid IP or DNS name"""
    try:
        ip = ipaddress.ip_address(hostname)
        if isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return True
    except ValueError:
        # Additional check for IPv4 addresses in the format XXX.XXX.XXX.XXX
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
            parts = hostname.split(".")
            if all(0 <= int(part) <= 255 for part in parts):
                return True
            return False
        if re.match(r"^[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63})*$", hostname):
            return True
    return False


def get_ip(
    bind_ip: str | None,
    bind_network: str | None,
) -> str:
    """Returns IP to listen"""
    b_ip: ipaddress.IPv4Address | ipaddress.IPv6Address | None = None
    b_net: ipaddress.IPv4Network | ipaddress.IPv6Network | None = None

    try:
        if bind_ip:
            b_ip = ipaddress.ip_address(bind_ip)
        if bind_network:
            b_net = ipaddress.ip_network(bind_network)
    except ValueError as exc:
        raise GetIPException(str(exc)) from exc

    local_ips = list(map(ipaddress.ip_address, _get_local_ips()))

    return _get_bind_ip(b_ip, b_net, local_ips).compressed


def _get_bind_ip(
    bind_ip: ipaddress.IPv4Address | ipaddress.IPv6Address | None,
    bind_network: ipaddress.IPv4Network | ipaddress.IPv6Network | None,
    local_ips: Sequence[ipaddress.IPv4Address | ipaddress.IPv6Address],
) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    """Get the IP listen to on the host"""
    if bind_ip:
        if bind_ip.is_link_local or bind_ip.is_unspecified:
            return bind_ip
        if bind_ip not in local_ips:
            raise GetIPException(f"{bind_ip!r} is not configured on this host. Unable to use.")
        return bind_ip
    if bind_network:
        for local_ip in local_ips:
            if local_ip in bind_network:
                return local_ip
        raise GetIPException(
            f"None of the local IPs belongs to {bind_network.compressed!r} network. Please specify bind IP instead"
        )
    return ipaddress.ip_address("0.0.0.0")


def _get_local_ips() -> Sequence[str]:
    """Get all IPs available on all interfaces"""
    addresses = []
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family in (socket.AF_INET, socket.AF_INET6):
                addresses.append(addr.address)
    return addresses
