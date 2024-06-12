from __future__ import annotations

from licensespring.api.signature import SignatureVerifier
from licensespring.hardware import HardwareIdProvider


class Configuration:
    """
    A class to configure settings for a license management system.

    This class encapsulates various configuration settings used for managing
    licenses, including authentication keys, encryption settings, hardware ID
    providers, signature verification, and API details.

    Attributes:
        product (str): Name of the product.
        api_key (str): API key for authentication.
        shared_key (str): Shared key for additional security.
        file_key (str): Encryption key for license files. Default is a sample key.
        file_iv (str): Initialization vector for encryption. Default is a sample vector.
        hardware_id_provider (object): Provider class for hardware ID. Default is HardwareIdProvider.
        verify_license_signature (bool): Flag to enable/disable signature verification. Default is True.
        signature_verifier (object): Verifier class for checking signatures. Default is SignatureVerifier.
        api_domain (str): Domain for the API server. Default is "api.licensespring.com".
        api_version (str): Version of the API. Default is "v4".
        filename (str): Name for the license file. Default is "License".
        file_path (str): Path to save the license file. Default is None.
        grace_period_conf (int): Grace period configuration in days. Default is 12.
        is_guard_file_enabled (bool): Enables guard protection for offline licenses if set to True.
    """

    def __init__(
        self,
        product: str,
        api_key: str,
        shared_key: str,
        file_key: str,
        file_iv: str,
        hardware_id_provider=HardwareIdProvider,
        verify_license_signature=True,
        signature_verifier=SignatureVerifier,
        api_domain="api.licensespring.com",
        api_version="v4",
        filename="License",
        file_path=None,
        grace_period_conf=24,
        is_guard_file_enabled=True,
    ) -> None:
        self._product = product

        self._api_key = api_key
        self._shared_key = shared_key

        self._file_key = file_key
        self._file_iv = file_iv

        self._hardware_id_provider = hardware_id_provider

        self._verify_license_signature = verify_license_signature
        self._signature_verifier = signature_verifier
        self._api_domain = api_domain
        self._api_version = api_version

        self._filename = filename
        self._file_path = file_path
        self.grace_period_conf = grace_period_conf
        self.is_guard_file_enabled = is_guard_file_enabled
