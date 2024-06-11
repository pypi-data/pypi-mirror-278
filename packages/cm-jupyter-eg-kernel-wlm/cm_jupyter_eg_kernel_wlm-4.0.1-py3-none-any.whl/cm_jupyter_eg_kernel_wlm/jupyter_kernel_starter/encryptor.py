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

import json
import os
import typing
from base64 import b64decode, b64encode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.conn_file import KernelConnectionInfo
from cm_jupyter_eg_kernel_wlm.jupyter_kernel_starter.consts import API_VERSION


class EncryptedConnectionInfo(typing.NamedTuple):
    """Structure to send to JEG or Kernel Provisioner to establish connection"""

    version: str
    connection_info: str  # encrypted connection info
    aes_key: str  # encrypted AES key
    iv: str  # initialization vector for AES


class EncryptedMessage(typing.NamedTuple):
    """Structure for incoming messages"""

    msg: str
    iv: str


class EncryptorDecryptor:
    """Handle secure connection based on provided public RSA key"""

    def __init__(self, server_public_key: PublicKeyTypes):
        self.server_public_key = server_public_key
        self.aes_key = os.urandom(32)  # Using 256-bit key for AES.

    def message_encrypt(self, message: str) -> EncryptedMessage:
        """Encrypt data. Return initialization vector and encrypted data."""
        iv = os.urandom(16)  # AES block size is 16 bytes.
        aesgcm = AESGCM(self.aes_key)
        encrypted_data = aesgcm.encrypt(iv, message.encode("utf-8"), None)
        return EncryptedMessage(
            msg=b64encode(encrypted_data).decode("utf-8"),
            iv=b64encode(iv).decode("utf-8"),
        )

    def encrypt_connection_info(self, kernel_connection_info: KernelConnectionInfo) -> EncryptedConnectionInfo:
        """Encrypt connection info using RSA and AES encryption.
        AES key is enrypted by public key of the server and connection_info id encrypted by AES key.
        So to decrypt server needs to use its RSA private key to get AES key and then decrypt
        connection info with AES key and IV"""
        if not isinstance(self.server_public_key, rsa.RSAPublicKey):
            raise ValueError(f"Unsupported public key type: {type(self.server_public_key).__name__}")

        conn_info_json = json.dumps(kernel_connection_info._asdict())
        encrypted_conn_info = self.message_encrypt(conn_info_json)

        rsa_encryptor = rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
        encrypted_aes_key = self.server_public_key.encrypt(self.aes_key, rsa_encryptor)

        return EncryptedConnectionInfo(
            version=API_VERSION,
            connection_info=encrypted_conn_info.msg,
            aes_key=b64encode(encrypted_aes_key).decode("utf-8"),
            iv=encrypted_conn_info.iv,
        )

    def message_decrypt(self, encrypted_message: EncryptedMessage) -> str:
        """Decrypt message."""
        iv = b64decode(encrypted_message.iv)
        encrypted_data = b64decode(encrypted_message.msg)
        aesgcm = AESGCM(self.aes_key)
        return aesgcm.decrypt(iv, encrypted_data, None).decode("utf-8")
