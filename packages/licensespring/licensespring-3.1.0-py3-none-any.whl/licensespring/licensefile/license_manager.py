import logging

import requests

from licensespring.api import APIClient
from licensespring.licensefile import License
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.customer import Customer
from licensespring.licensefile.data_storage import DataStorage
from licensespring.licensefile.offline_activation_guard import (
    OfflineActivation,
    OfflineActivationGuard,
)


class LicenseID:
    """
    Represents a mechanism for license identification and activation.

    The LicenseID class provides a structured way to handle both key-based and user-based
    license activations. It encapsulates the necessary details for each activation method,
    allowing for clear and concise license management within applications.

    Attributes:
        key (str, optional): The license key for key-based activation. Defaults to None.
        username (str, optional): The username (typically an email) for user-based activation. Defaults to None.
        password (str, optional): The password associated with the username for user-based activation. Defaults to None.

    Methods:
        from_key: Class method to create a LicenseID instance for key-based activation.
        from_user: Class method to create a LicenseID instance for user-based activation.
    """

    def __init__(self) -> None:
        self.key = None
        self.username = None
        self.password = None

    @classmethod
    def from_key(cls, key):
        """
        Creates an instance of LicenseID for a key-based license.

        Parameters:
            key (str): license key

        Returns:
            LicenseID
        """
        licenseID = cls()
        licenseID.key = key
        return licenseID

    @classmethod
    def from_user(cls, username, password):
        """
        Creates an instance of LicenseID for a user-based license.

        Parameters:
            username (str): email of an user
            password (str): password

        Returns:
            LicenseID
        """
        licenseID = cls()
        licenseID.username = username
        licenseID.password = password
        return licenseID


class LicenseManager:
    """
    LicenseManager is used for license activation

    Attributes:
        api_client (APIClient): An instance of the APIClient responsible for API communication.
        _product (str): LicenseSpring product.
        licensefile_handler (DataStorage): A data storage handler for managing
            license file operations.

    Parameters:
        conf (Configuration): A configuration object containing necessary parameters
            such as API keys, hardware ID provider, and other settings required
            for license activation and verification.
    """

    def __init__(
        self,
        conf: Configuration,
    ) -> None:
        self.api_client = APIClient(
            api_key=conf._api_key,
            shared_key=conf._shared_key,
            hardware_id_provider=conf._hardware_id_provider,
            verify_license_signature=conf._verify_license_signature,
            signature_verifier=conf._signature_verifier,
            api_domain=conf._api_domain,
            api_version=conf._api_version,
        )

        self._product = conf._product

        self.licensefile_handler = DataStorage(conf=conf)

    def load_license(self) -> License:
        """
        Loads licensefile and sets attributes for LicenseData instance
        Returns:
        License: An instance of the License class reflecting the loaded license.
        """
        self.licensefile_handler.load_licensefile()

        return License(self._product, self.api_client, self.licensefile_handler)

    def activate_license(
        self,
        license_id: LicenseID,
        bundle_code: str = None,
        hardware_id: str = None,
        customer_account_code: str = None,
        id_token: str = None,
        code: str = None,
        app_ver: str = None,
        os_ver: str = None,
        hostname: str = None,
        ip: str = None,
        is_vm: bool = None,
        vm_info: str = None,
        mac_address: str = None,
    ) -> License:
        """
        Activates a license with the license server and updates local license data accordingly.

        This method supports a variety of parameters to accommodate different licensing scenarios,
        including key-based activation, user-based activation

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
            bundle_code (str, optional): specify unique bundle_code of a bundle
            hardware_id (str, optional): A unique identifier for the hardware.
            customer_account_code (str, optional): An account code for the customer.
            id_token (str, optional): Token for identity verification.
            code (str, optional): An additional code for license verification.
            app_ver (str, optional): The version of the application requesting activation.
            os_ver (str, optional): The operating system version of the host.
            hostname (str, optional): The hostname of the device requesting activation.
            ip (str, optional): The IP address of the device.
            is_vm (bool, optional): Indicates whether the application is running on a virtual machine.
            vm_info (str, optional): Information about the virtual machine, if applicable.
            mac_address (str, optional): The MAC address of the device.

        Returns:
            License: An instance of the License class reflecting the activated license.
        """

        response = self.api_client.activate_license(
            product=self._product,
            bundle_code=bundle_code,
            hardware_id=hardware_id,
            license_key=license_id.key,
            username=license_id.username,
            password=license_id.password,
            customer_account_code=customer_account_code,
            id_token=id_token,
            code=code,
            app_ver=app_ver,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            is_vm=is_vm,
            vm_info=vm_info,
            mac_address=mac_address,
        )

        response["username"] = license_id.username
        response["bundle_code"] = bundle_code
        self.licensefile_handler._cache.update_cache("activate_license", response)
        self.licensefile_handler.save_licensefile()

        return License(
            self._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )

    def is_online(self) -> bool:
        response = requests.get(
            f"{self.api_client.api_protocol}://{self.api_client.api_domain}"
        )

        if response.status_code == 200:
            return True

        return False

    def create_offline_activation_file(
        self,
        license_id: LicenseID,
        req_path: str,
        bundle_code: str = None,
        hardware_id: str = None,
        app_ver: str = None,
        os_ver: str = None,
        hostname: str = None,
        ip: str = None,
        is_vm: bool = None,
        vm_info: str = None,
        mac_address: str = None,
    ) -> str:
        """
        Creates .req file for activation

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
            req_path (str): Specify place where to create .req file
            bundle_code (str, optional): specify unique bundle_code of a bundle.
            hardware_id (str, optional): A unique identifier for the hardware.
            app_ver (str, optional): The version of the application requesting activation.
            os_ver (str, optional): The operating system version of the host.
            hostname (str, optional): The hostname of the device requesting activation.
            ip (str, optional):  The IP address of the device.
            is_vm (bool, optional): Indicates whether the application is running on a virtual machine.
            vm_info (str, optional): Information about the virtual machine.
            mac_address (str, optional): The MAC address of the device.

        Returns:
            str: path of the .req file
        """

        data = self.api_client.activate_offline_dump(
            product=self._product,
            bundle_code=bundle_code,
            hardware_id=hardware_id,
            license_key=license_id.key,
            username=license_id.username,
            password=license_id.password,
            app_ver=app_ver,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            is_vm=is_vm,
            vm_info=vm_info,
            mac_address=mac_address,
        )

        offline_data = OfflineActivation()
        offline_data.set_data(data)
        offline_data.set_is_activation(True)
        offline_data.create_guard_file(
            self.licensefile_handler.create_activation_guard(
                offline_data.decode_offline_activation()["request_id"]
            )
        )

        return self.licensefile_handler.create_request_file(
            req_data=offline_data, offline_path=req_path
        )

    def activate_license_offline(self, ls_activation_path: str) -> License:
        """
        Activates a .lic

        Args:
            ls_activation_path (str): path to activation file

        Raises:
            LicenseActivationException: Activation data is not valid
            LicenseActivationException: Response file ID mismatch
            LicenseActivationException: License does not belong to this device

        Returns:
            License: License object
        """

        offline_data = OfflineActivation()
        data = self.licensefile_handler.load_offline_response(ls_activation_path)
        offline_data.set_data(data)
        offline_data.set_is_activation(True)
        offline_data.set_use_guard(self.licensefile_handler._conf.is_guard_file_enabled)

        if len(offline_data._data) == 0:
            return

        response = offline_data.decode_offline_activation()
        logging.info("Offline file activation id:", response["request_id"])

        if self.licensefile_handler._conf.is_guard_file_enabled:
            guard_dict = self.licensefile_handler.load_guard_file()
            offline_data.create_guard_file(OfflineActivationGuard.from_json(guard_dict))
            self.licensefile_handler.check_guard(offline_data)

        self.licensefile_handler._cache.update_cache(
            "activate_license_offline", response
        )
        license = License(
            self._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )
        license.licensefile_handler.save_licensefile()
        self.licensefile_handler.remove_offline_activation_data(ls_activation_path)
        logging.info("Offline activation succeeded")

        return license

    def get_trial_license(
        self, customer: Customer, license_policy: str = None
    ) -> LicenseID:
        """
        Creates LiceseID for trial licenses

        Args:
            customer (Customer): Customer object
            license_policy (str, optional): license policy code. Defaults to None.

        Returns:
            LicenseID
        """

        response = self.api_client.trial_key(
            self._product,
            hardware_id=None,
            email=customer.email,
            license_policy=license_policy,
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone=customer.phone,
            address=customer.address,
            postcode=customer.postcode,
            state=customer.state,
            country=customer.country,
            city=customer.city,
            reference=customer.reference,
        )

        if "license" in response:
            return LicenseID.from_key(response["license"])

        else:
            return LicenseID.from_user(
                response["license_user"], response["initial_password"]
            )
