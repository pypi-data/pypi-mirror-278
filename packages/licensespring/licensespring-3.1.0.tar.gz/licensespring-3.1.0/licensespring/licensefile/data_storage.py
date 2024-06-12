from __future__ import annotations

import base64
import json
import logging
import os
from datetime import datetime, timezone

from licensespring.licensefile.config import Configuration
from licensespring.licensefile.default_crypto import DefaultCryptoProvider
from licensespring.licensefile.error import (
    ErrorType,
    LicenseActivationException,
    LicenseDeleted,
)
from licensespring.licensefile.license_data import LicenseData
from licensespring.licensefile.offline_activation_guard import (
    OfflineActivation,
    OfflineActivationGuard,
)


class DataStorage(DefaultCryptoProvider):
    """
    Extends DefaultCryptoProvider to handle license file cache operations, including saving to and loading from a .key file.

    Attributes:
        _conf (Configuration): Configuration object containing settings and parameters.
        _cache (LicenseData): Instance of LicenseData for managing license attributes in memory.
        _filename (str): The name of the file used for storing the license information.
        _license_path (str): The file path where the license file is stored.

    Methods:
        cache: Returns the current license data stored in memory.
        license_path: Returns the file path for the license file.
        save_licensefile(): Encrypts and saves the license data to a file.
        load_licensefile(): Loads and decrypts the license data from a file.
        set_path(product_code, custom_path): Sets the file path for the license file based on the operating system.
        delete_licensefile(): Deletes the license file and clears the license data in memory.
        create_activation_guard(id): Creates OfflineActivationGuard object.
        create_request_file(req_data,offline_path): Creates .req file for license activation or deactivation.
        save_guard_file(guard): Saves guard file locally.
        remove_offline_activation_data(activation_file): Removes guard and activation file.
        load_guard_file(): Loads locally saved guard file.
        check_guard(offline_data): Checks the validity of the .lic file.
        load_offline_response(file_path): Loads offline response file.
    """

    def __init__(self, conf: Configuration):
        self._conf = conf
        super().__init__(self._conf._file_key, self._conf._file_iv)

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )

        self._filename = self._conf._filename
        self._license_path = self.set_path(self._conf._product, self._conf._file_path)

    @property
    def cache(self):
        return self._cache.to_json()

    @property
    def license_path(self):
        return self._license_path

    def save_licensefile(self):
        """
        Creates path for licensefile
        Saves encrypted string of licensefile JSON
        """

        json_string_encrypted = self.encrypt(self._cache.to_json())
        with self._cache._lock:
            if not os.path.exists(self.license_path):
                os.makedirs(self.license_path)

            with open(
                os.path.join(self.license_path, self._filename + ".key"), "w"
            ) as file:
                file.write(json_string_encrypted)

    def create_activation_guard(self, id: str) -> OfflineActivationGuard:
        """
        Creates OfflineActivationGuard object

        Args:
            id (str): response_id

        Returns:
            OfflineActivationGuard
        """

        offline_guard = OfflineActivationGuard()
        offline_guard.set_id(id=id)
        offline_guard.set_device_id(self._conf._hardware_id_provider.get_id(self))
        offline_guard.set_date_created()

        return offline_guard

    def create_request_file(
        self, req_data: OfflineActivation, offline_path: str
    ) -> str:
        """
        Creates .req file for license activation or deactivation

        Args:
            req_data (OfflineActivation): OfflineActivation object
            offline_path (str): sets a path for .req file

        Returns:
            str: path of a .req file
        """

        if not os.path.exists(offline_path):
            os.makedirs(offline_path)

        filename = (
            "activate_offline.req"
            if req_data._is_activation
            else "deactivate_offline.req"
        )

        with open(os.path.join(offline_path, filename), mode="w") as f:
            print(req_data._data, file=f)

        if req_data._is_activation:
            self.save_guard_file(req_data._guard)

        return os.path.join(offline_path, filename)

    def save_guard_file(self, guard: OfflineActivationGuard) -> None:
        """
        Saves guard file locally

        Args:
            guard (OfflineActivationGuard): OfflineActivationGuard object
        """

        if self._conf.is_guard_file_enabled:
            self.remove_offline_activation_data()
            with open(
                os.path.join(self.license_path, "OfflineActivation.guard"), "w"
            ) as file:
                file.write(self.encrypt(guard.to_json()))

    def remove_offline_activation_data(self, activation_file: str = None):
        """
        Removes guard and activation file.

        Args:
            activation_file (str, optional): Path of the activation file. Defaults to None.
        """

        file_path_guard = os.path.join(self.license_path, "OfflineActivation.guard")

        if os.path.exists(file_path_guard):
            os.remove(file_path_guard)

        if activation_file != None:
            if os.path.exists(activation_file):
                os.remove(activation_file)

    def load_guard_file(self) -> dict:
        """
        Loads locally saved guard file

        Returns:
            dict: guard file
        """

        with open(
            os.path.join(self.license_path, "OfflineActivation.guard"), "r"
        ) as file:
            json_string_encrypted = file.read()

        return json.loads(self.decrypt(json_string_encrypted))

    def check_guard(self, offline_data: OfflineActivation):
        """
        Checks the validity of the .lic file

        Args:
            offline_data (OfflineActivation): OfflineActivation object

        Raises:
            LicenseActivationException: Activation data is not valid
            LicenseActivationException: Response file ID mismatch
            LicenseActivationException: License does not belong to this device
        """

        decoded_data = offline_data.decode_offline_activation()

        if offline_data._guard._date_created > datetime.now(timezone.utc).replace(
            tzinfo=None
        ):
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "Activation data is not valid, please restart activation process.",
            )

        elif offline_data._guard._id != decoded_data["request_id"]:
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "Response file ID mismatch, please restart activation process.",
            )

        elif offline_data._guard._device_id != self._conf._hardware_id_provider.get_id(
            self
        ):
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "License does not belong to this device.",
            )

    def load_offline_response(self, file_path: str) -> str:
        """
        Loads offline response file

        Args:
            file_path (str): file path

        Returns:
            str: string data
        """

        file_path = os.path.join(file_path)

        with open(file_path, "r") as file:
            data = file.read()

        return data

    def load_licensefile(self) -> dict:
        """
        Loads and decrypts licensefile

        Returns:
            dict: licensefile
        """

        try:
            with open(
                os.path.join(self.license_path, self._filename + ".key"), "r"
            ) as file:
                json_string_encrypted = file.read()

            licensefile_dict = json.loads(self.decrypt(json_string_encrypted))

            self._cache.from_json_to_attr(licensefile_dict)

            self._cache.grace_period_conf = self._conf.grace_period_conf

            return licensefile_dict

        except FileNotFoundError:
            raise LicenseDeleted(ErrorType.NO_LICENSEFILE, "Licensefile doesn't exist")

    def set_path(self, product_code: str, custom_path=None) -> str:
        """
        Set path for licensefile

        Parameters:
            product_code (str): short product code of LicenseSpring product
            custom_path(str,optional): custom path of licensefile

        Returns:
            str: Path of licensefile
        """

        if custom_path is not None:
            return custom_path

        if os.name == "nt":  # Windows
            base_path = os.path.join(
                os.environ.get("SystemDrive"), "Users", os.environ.get("USERNAME")
            )
            return os.path.join(
                base_path, "AppData", "Local", "LicenseSpring", product_code
            )

        elif os.name == "posix":  # Linux and macOS
            if "HOME" in os.environ:
                base_path = os.environ["HOME"]
                return os.path.join(
                    base_path, ".LicenseSpring", "LicenseSpring", product_code
                )

            else:  # macOS and other POSIX systems
                base_path = os.path.expanduser("~")
                return os.path.join(
                    base_path,
                    "Library",
                    "Application Support",
                    "LicenseSpring",
                    product_code,
                )

        else:
            raise Exception("Unsupported operating system")

    def delete_licensefile(self):
        """
        Permanently deletes licensefile and clears cache

        Returns: None
        """

        self.remove_offline_activation_data()

        if os.path.exists(os.path.join(self.license_path)):
            os.remove(os.path.join(self.license_path, self._filename + ".key"))

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )
