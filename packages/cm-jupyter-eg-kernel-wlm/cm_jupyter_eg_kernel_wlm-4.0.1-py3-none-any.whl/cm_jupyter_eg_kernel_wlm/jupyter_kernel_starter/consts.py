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
"""Number of constants"""

API_VERSION = "2"
CONNECTION_FILE_PLACEHOLDER = "__connection_file__"

MAX_PORT = 2**16
KERNEL_MIN_PORTS_REQUIRED = 5
KERNEL_TRANSPORT = "tcp"
KERNEL_SIGNATURE_SCHEME = "hmac-sha256"
KERNEL_HMAC_KEY_LEN = 16
HANDLER_SOCKET_BACKLOG_LEN = 5
HANDLER_QUEUE_SIZE = 10
HANDLER_DATA_BUFF_SIZE = 1024
