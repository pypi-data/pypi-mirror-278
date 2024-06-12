from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Callable

from requests.exceptions import RequestException

from licensespring.api.error import ClientError
from licensespring.licensefile.error import (
    ClockTamperedException,
    ConfigurationMismatch,
    ErrorType,
    LicenseStateException,
    TimeoutExpiredException,
    VMIsNotAllowedException,
)
from licensespring.licensefile.offline_activation_guard import OfflineActivation
from licensespring.watchdog import LicenseWatchdog


class License:
    """
    Represents and manages license operations including activation, deactivation,
    and consumption tracking for a software product.

    Methods:
        __init__(self, product, api_client, licensefile_handler): Initializes the license object with a product, API client, and licensefile handler.
        is_floating_expired(self): Checks if a floating license has expired. Placeholder method that currently always returns False.
        is_validity_period_expired(self): Determines whether the license's validity period has expired, based on the enabled state and validity period.
        check_license_status(self): Verifies the current status of the license, raising exceptions if the license is not enabled, not active, or expired.
        check(self, include_expired_features=False, req_overages=-1): Performs an online check to sync license data with the backend
        deactivate(self, delete_license=False): Deactivates the license and optionally deletes the local license file.
        local_check(self): Performs a local check of the license against product code, hardware ID, and VM restrictions.
        add_local_consumption(self, consumptions=1): Adds local consumption records for consumption-based licenses,
        sync_consumption(self, req_overages=-1): Syncs local consumption data with the server, adjusting for overages if specified.
        is_grace_period(self, e: Exception): Determines if the current license state is within a grace period
        setup_license_watch_dog(self,callback,timeout):Initializes and starts the license watchdog with the specified callback and timeout.
        stop_license_watch_dog(self): Stops the license watchdog if it is currently running.
        floating_borrow(self,borrow_until:str): Attempts to borrow a floating license until the specified date.
        floating_release(self,throw_e:bool): Releases a borrowed floating license and updates the license status accordingly.


    Attributes:
        product (str): The software product this license is associated with.
        api_client: An instance responsible for communicating with the licensing API.
        licensefile_handler: Handles local license file operations such as reading and writing.
    """

    def __init__(self, product, api_client, licensefile_handler) -> None:
        self.product = product
        self.api_client = api_client
        self.licensefile_handler = licensefile_handler
        self.watch_dog = None

    def is_floating_expired(self) -> bool:
        if self.licensefile_handler._cache.is_floating_license():
            return self.licensefile_handler._cache.floating_period < datetime.now(
                timezone.utc
            ).replace(tzinfo=None)
        return False

    def is_validity_period_expired(self) -> bool:
        """
        Determines whether the license's validity period has expired.

        Returns:
            bool: True if the validity period has expired or the license is disabled, False otherwise.
        """

        if self.licensefile_handler._cache.is_expired:
            return True

        if isinstance(self.licensefile_handler._cache.validity_period, datetime):
            if (
                self.licensefile_handler._cache.validity_with_grace_period()
                < datetime.now(timezone.utc).replace(tzinfo=None)
            ):
                self.licensefile_handler._cache.set_boolean("is_expired", True)

                return True

        return False

    def check_license_status(self) -> None:
        """
        Verifies the current status of the license, including its enablement, activation, and expiration.

        Raises:
            LicenseStateException: If the license is not enabled, not active, or expired.
        """

        if not self.licensefile_handler._cache.license_enabled:
            raise LicenseStateException(
                ErrorType.LICENSE_NOT_ENABLED, "The license disabled"
            )

        if not self.licensefile_handler._cache.license_active:
            raise LicenseStateException(
                ErrorType.LICENSE_NOT_ACTIVE, "The license is not active."
            )

        if self.is_validity_period_expired():
            raise LicenseStateException(
                ErrorType.LICENSE_EXPIRED, "The license is expired."
            )

    def check(self, include_expired_features=False) -> dict | None:
        """
        Performs an online license check, syncing the license data with the backend.
        This includes syncing consumptions for consumption-based licenses.

        Args:
            include_expired_features (bool, optional): If True, includes expired license features in the check.
                Defaults to False.
            req_overages (int, optional): Specifies the behavior for consumption overages.
                Use -1 to ignore, 0 to disable overages, and a positive value to enable overages
                up to the specified value. Defaults to -1.

        Returns:
            dict: The response from the license check operation.

        Raises:
            Exceptions: Various exceptions can be raised depending on the API client's implementation and the response from the licensing server.
        """

        try:
            # Add logic for floating server
            logging.info("Online check started")

            response = self.api_client.check_license(
                product=self.licensefile_handler._cache.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
                include_expired_features=include_expired_features,
            )

            self.licensefile_handler._cache.update_cache("check_license", response)
            self.licensefile_handler._cache.update_floating_period(
                self.licensefile_handler._cache.borrowed_until
            )

            for (
                feature
            ) in self.licensefile_handler._cache.feature_manager.return_features_list():
                self.sync_feature_consumption(feature)

            if self.licensefile_handler._cache.license_type == "consumption":
                self.sync_consumption(req_overages=-1)

            self.licensefile_handler._cache.reset_grace_period_start_date()

            logging.info("Online check successful")

            return response

        except ClientError as ex:
            self.licensefile_handler._cache.update_from_error_code(ex.code)

            logging.info(ex)
            raise ex

        except RequestException as ex:
            if (
                not self.licensefile_handler._cache.is_floating_license()
                or self.licensefile_handler._cache.is_active_floating_cloud()
            ) and self.is_grace_period(ex):
                return None

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        finally:
            self.licensefile_handler.save_licensefile()
            self.check_license_status()

    def deactivate(self, delete_license=False) -> None:
        """
        Deactivates the license and optionally deletes the local license file.

        Args:
            delete_license (bool, optional): If True, deletes the local license file upon deactivation.
                Defaults to False.
        """

        if not self.licensefile_handler._cache.license_active:
            if delete_license:
                self.licensefile_handler.delete_licensefile()
            return None

        self.api_client.deactivate_license(
            product=self.licensefile_handler._cache.product,
            bundle_code=getattr(self.licensefile_handler._cache, "bundle_code", None),
            hardware_id=None,
            license_key=getattr(self.licensefile_handler._cache, "license_key", None),
            username=getattr(self.licensefile_handler._cache, "username", None),
        )

        if delete_license:
            self.licensefile_handler.delete_licensefile()
            return None

        self.licensefile_handler._cache.deactivate()
        self.licensefile_handler.save_licensefile()

    def local_check(self) -> None:
        """
        Performs a local check of the license, ensuring product code, hardware ID, VM (virtual machine), and other conditions are met.

        Raises:
            Various exceptions for different failure conditions.
        """
        try:
            if self.licensefile_handler._cache.product != self.product:
                raise ConfigurationMismatch(
                    ErrorType.PRODUCT_MISMATCH,
                    "License product code does not correspond to configuration product code",
                )

            if (
                self.licensefile_handler._cache.hardware_id
                != self.api_client.hardware_id_provider.get_id()
            ):
                raise ConfigurationMismatch(
                    ErrorType.HARDWARE_ID_MISMATCH,
                    "License hardware id does not correspond to configuration hardware id",
                )

            self.check_license_status()

            if (
                self.api_client.hardware_id_provider.get_is_vm()
                != self.licensefile_handler._cache.prevent_vm
            ):
                raise VMIsNotAllowedException(
                    ErrorType.VM_NOT_ALLOWED, "Virtual machine not allowed."
                )

            if self.is_floating_expired():
                raise TimeoutExpiredException(
                    ErrorType.FLOATING_TIMEOUT, "Floating license timeout has expired."
                )

            if self.licensefile_handler._cache.last_usage > datetime.now(
                timezone.utc
            ).replace(tzinfo=None):
                raise ClockTamperedException(
                    ErrorType.CLOCK_TAMPERED, "Detected cheating with local date time."
                )

        except LicenseStateException as e:
            self.licensefile_handler._cache.update_from_error_code(e.error_type.name)

            raise e

    def change_password(self, password: str, new_password: str) -> str:
        """
        Changes the password for user-based license.
        This method first checks the current license status to ensure it is active and not expired.
        It then attempts to change the password with the licensing server.

        Params:
            password (str): Old password of license user
            new_password (str): New password of license user

        Returns:
            str: password was changed.
        """

        self.check_license_status()

        response = self.api_client.change_password(
            username=getattr(self.licensefile_handler._cache, "username", None),
            password=password,
            new_password=new_password,
        )

        return response

    def add_local_consumption(self, consumptions=1) -> None:
        """
        Adds local consumption to the license
        Params:
            consumptions (int,optional): Number of consumptions.

        Returns: None
        """

        self.licensefile_handler._cache.update_consumption(consumptions)

    def add_local_feature_consumption(self, feature: str, consumptions=1) -> None:
        """
        Adds local consumption to the feature.
        Params:
            feature (str): feature code.
            consumptions (int,optional): Number of consumptions.
        """

        self.licensefile_handler._cache.update_feature_consumption(
            feature, consumptions
        )

    def sync_feature_consumption(self, feature) -> bool:
        """
        Syncs the local consumption data with the server for consumption-based licenses.

        Args:
            feature (str): feature code.

        Returns:
            bool: True if the consumption data was successfully synchronized; False otherwise.

        """

        if not hasattr(self.licensefile_handler._cache.feature_manager, feature):
            return False

        feature_obj = getattr(self.licensefile_handler._cache.feature_manager, feature)

        if not hasattr(feature_obj, "local_consumption"):
            return False

        if feature_obj.local_consumption == 0:
            return False

        try:
            response = self.api_client.add_feature_consumption(
                product=self.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
                feature=feature,
                consumptions=feature_obj.local_consumption,
            )

        except ClientError as ex:
            logging.info(ex)
            raise ex

        except RequestException as ex:
            if self.is_grace_period(ex):
                self.licensefile_handler.save_licensefile()
                self.check_license_status()

                return False

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        else:
            self.licensefile_handler._cache.update_cache(
                "feature_consumption", response, feature
            )

            self.licensefile_handler._cache.reset_grace_period_start_date()

            self.licensefile_handler.save_licensefile()

            return True

    def sync_consumption(self, req_overages=-1) -> bool:
        """
        Syncs the local consumption data with the server for consumption-based licenses.

        Args:
            req_overages (int, optional): Specifies the behavior for requesting consumption overages.
                Defaults to -1, which means no overage request is made. A value of 0 disables overages,
                and a positive value requests permission for overages up to the specified value.

        Returns:
            bool: True if the consumption data was successfully synchronized; False otherwise.

        Side Effects:
            Resets local consumption count after successful synchronization.
        """

        if not hasattr(self.licensefile_handler._cache, "local_consumption"):
            return False

        if self.licensefile_handler._cache.local_consumption == 0 and req_overages < 0:
            return False

        try:
            if req_overages == 0:
                max_overages = req_overages
                allow_overages = False

            elif req_overages > 0:
                max_overages = req_overages
                allow_overages = True

            else:
                max_overages = None
                allow_overages = None

            response = self.api_client.add_consumption(
                product=self.licensefile_handler._cache.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
                consumptions=self.licensefile_handler._cache.local_consumption,
                max_overages=max_overages,
                allow_overages=allow_overages,
            )

        except ClientError as ex:
            logging.info(ex)
            raise ex

        except RequestException as ex:
            if self.is_grace_period(ex):
                self.licensefile_handler.save_licensefile()
                self.check_license_status()

                return False

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        else:
            self.licensefile_handler._cache.update_cache(
                "license_consumption", response
            )

            self.licensefile_handler._cache.reset_grace_period_start_date()
            self.licensefile_handler.save_licensefile()

            return True

    def is_grace_period(self, ex: Exception) -> bool:
        """
        Determines if the license is currently within its grace period following a specific exception.
        The grace period logic is activated only if the license cache has a 'grace_period' attribute set,
        and the passed exception is of type 'RequestException', typically indicating a communication
        error with the licensing server.

        Returns:
            bool: True if the license is within its grace period, False otherwise.

        Side Effects:
            - If the license is within its grace period and a 'RequestException' occurs, this method
            updates the grace period start date in the license cache to the current time.
        """

        if not hasattr(self.licensefile_handler._cache, "grace_period_conf"):
            return False

        elif self.licensefile_handler._cache.grace_period_conf > 0 and isinstance(
            ex, RequestException
        ):
            self.licensefile_handler._cache.update_grace_period_start_date()

            return (
                datetime.now(timezone.utc).replace(tzinfo=None)
                < self.licensefile_handler._cache.grace_period_end_date()
            )

        return False

    def setup_license_watch_dog(self, callback: Callable, timeout: int) -> None:
        """
        Initializes and starts the license watchdog with the specified callback and timeout.

        Args:
            callback: A callable to be executed by the watchdog in response to specific events or conditions.
            timeout: The period in minutes after which the watchdog should perform its checks.

        Side Effects:
            - Instantiates the LicenseWatchdog class and stores the instance.
            - Starts the watchdog thread.
        """

        self.watch_dog = LicenseWatchdog(self, callback, timeout)
        self.watch_dog.run()

    def stop_license_watch_dog(self) -> None:
        """
        Stops the license watchdog if it is currently running.

        Side Effects:
            - Stops the watchdog thread, if it exists.
        """

        if self.watch_dog:
            self.watch_dog.stop()

    def floating_borrow(self, borrow_until: str, password: str = None) -> None:
        """
        Attempts to borrow a floating license until the specified date.

        Args:
            borrow_until: A string representing the date until which the license should be borrowed.

        Returns:
            None

        Side Effects:
            - Checks if the license is floating or floating cloud type and attempts to borrow it.
            - Updates the license cache and stops the license watchdog if borrowing is successful.
        """

        if not self.licensefile_handler._cache.is_floating_license():
            return None

        response = self.api_client.floating_borrow(
            product=self.licensefile_handler._cache.product,
            bundle_code=getattr(self.licensefile_handler._cache, "bundle_code", None),
            hardware_id=None,
            license_key=getattr(self.licensefile_handler._cache, "license_key", None),
            username=getattr(self.licensefile_handler._cache, "username", None),
            password=password,
            borrowed_until=borrow_until,
        )

        self.licensefile_handler._cache.set_boolean("is_borrowed", True)
        self.stop_license_watch_dog()
        self.licensefile_handler._cache.update_cache("normal", response)
        self.licensefile_handler._cache.update_floating_period(
            self.licensefile_handler._cache.borrowed_until
        )
        self.licensefile_handler.save_licensefile()

    def floating_release(self, throw_e: bool):
        """
        Releases a borrowed floating license and updates the license status accordingly.

        Args:
            throw_e: A boolean indicating whether to raise an exception on failure.

        Returns:
            None

        Side Effects:
            - Attempts to release the floating license and update the license cache.
            - Logs and potentially raises an exception if an error occurs during release.
        """

        if not self.licensefile_handler._cache.is_floating_license():
            return None

        try:
            self.check_license_status()

            # Add logic for both floating cloud and floating license
            if self.licensefile_handler._cache.is_active_floating_cloud():
                self.api_client.floating_release(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

                self.licensefile_handler._cache.release_license()
                self.licensefile_handler.save_licensefile()

        except Exception as ex:
            if throw_e:
                logging.info(ex)
                raise ex

    def check_feature(self, feature: str, add_to_watchdog=False) -> None:
        """
        Checks for a specific license feature and updates the license cache accordingly.

        Args:
            feature: feature code.
            add_to_watchdog: A boolean indicating whether to add the feature check to a watchdog routine.

        Returns:
            None
        """
        # Add watchdog logic
        try:
            response = self.api_client.check_license_feature(
                product=self.licensefile_handler._cache.product,
                feature=feature,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
            )

            self.licensefile_handler._cache.register_feature(feature)
            self.licensefile_handler._cache.update_cache(
                "register_feature", response, feature
            )

            self.licensefile_handler.save_licensefile()

        except Exception as ex:
            logging.info(ex)
            raise ex

    def release_feature(self, feature: str):
        """
        Releases a borrowed license feature and updates the license cache accordingly.

        Args:
            feature: The feature code.

        Returns:
            None
        """

        # Add watchdog logic
        try:
            self.api_client.floating_feature_release(
                product=self.licensefile_handler._cache.product,
                feature=feature,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
            )

            self.licensefile_handler._cache.release_feature(feature)
            self.licensefile_handler.save_licensefile()

        except Exception as ex:
            logging.info(ex)
            raise ex

    def update_offline(self, path: str, reset_consumption: bool) -> bool:
        """
        Updates license via refresh file

        Args:
            path (str): path of the refresh file
            reset_consumption (bool): True resets consumption otherwise False

        Raises:
            ConfigurationMismatch: The update file does not belong to this device
            ConfigurationMismatch: The update file does not belong to this product

        Returns:
            bool: True if license was successfully updated otherwise False
        """

        data = self.licensefile_handler.load_offline_response(path)
        decoded_data = self.api_client.check_offline_load(data)

        if decoded_data["hardware_id"] != self.licensefile_handler._cache.hardware_id:
            raise ConfigurationMismatch(
                ErrorType.HARDWARE_ID_MISMATCH,
                " The update file does not belong to this device. ",
            )

        if (
            decoded_data["product_details"]["short_code"]
            != self.licensefile_handler._cache.product
        ):
            raise ConfigurationMismatch(
                ErrorType.PRODUCT_MISMATCH,
                " The update file does not belong to this product.",
            )

        if (
            reset_consumption == True
            and self.licensefile_handler._cache.license_type == "consumption"
        ):
            self.licensefile_handler._cache.reset_consumption()

        self.licensefile_handler._cache.update_cache(
            "update_license_offline", decoded_data
        )
        self.licensefile_handler.save_licensefile()

        return True

    def deactivate_offline(self, offline_path: str) -> str:
        """
        Generates .req file for the offline deactivation

        Args:
            offline_path (str): path of the .req file

        Returns:
            str: path of the deactivation file
        """

        self.licensefile_handler._cache.deactivate()
        data = self.api_client.deactivate_offline_dump(
            product=self.product,
            bundle_code=getattr(self.licensefile_handler._cache, "bundle_code", None),
            hardware_id=None,
            license_key=getattr(self.licensefile_handler._cache, "license_key", None),
            username=getattr(self.licensefile_handler._cache, "username", None),
        )
        offline_data = OfflineActivation()
        offline_data.set_is_activation(False)
        offline_data.set_data(data)

        return self.licensefile_handler.create_request_file(offline_data, offline_path)

    def product_details(
        self, include_latest_version: bool = False, include_custom_fields: bool = False
    ) -> dict:
        """
        Update product details from LicenseSpring server

        Args:
            include_latest_version (bool, optional): Lateset version information. Defaults to False.
            include_custom_fields (bool, optional): custom fields information. Defaults to False.

        Returns:
            dict: response
        """
        response = self.api_client.product_details(
            self.product, include_latest_version, include_custom_fields
        )

        self.licensefile_handler._cache.update_cache("product_details", response)
        self.licensefile_handler.save_licensefile()

        return response

    def set_device_variables(self, variables: dict, save: bool = True):
        """
        Set device variables locally

        Args:
            variables (dict): variables dict
            save (bool, optional): Save cache to licensefile. Defaults to True.
        """
        self.licensefile_handler._cache.set_variables(variables)
        if save:
            self.licensefile_handler.save_licensefile()

    def send_device_variables(self) -> bool:
        """
        Send device variables to LicenseSpring server. Handles GracePeriod

        Raises:
            ex: RequestException (Grace period not allowed)

        Returns:
            bool: True if new variables are sent to LicenseSpring server otherwise, False
        """
        try:
            new_varaibles = (
                self.licensefile_handler._cache.get_device_variables_for_send()
            )

            if len(new_varaibles) == 0:
                return False

            self.api_client.track_device_variables(
                product=self.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                username=getattr(self.licensefile_handler._cache, "username", None),
                variables=new_varaibles,
            )

            return True

        except RequestException as ex:
            if self.is_grace_period(ex):
                return False

            logging.info(ex)
            raise ex

    def get_device_variable(self, variable_name: str) -> dict:
        """
        Get device variable if exists

        Args:
            variable_name (str): variable name

        Returns:
            dict: variable dictionary
        """
        return self.licensefile_handler._cache.get_variable(variable_name)

    def get_device_variables(self, get_from_be: bool = True) -> list:
        """
        Get device variables from server or locally

        Args:
            get_from_be (bool, optional): If True collects data from LicenseSpring server. Defaults to True.

        Raises:
            ex: RequestException (Grace period not allowed)

        Returns:
            list: List of device variables
        """
        if get_from_be:
            try:
                response = self.api_client.get_device_variables(
                    product=self.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

            except RequestException as ex:
                if not self.is_grace_period():
                    logging.info(ex)
                    raise ex

            self.licensefile_handler._cache.update_cache("device_variables", response)
            self.licensefile_handler.save_licensefile()

        return self.licensefile_handler._cache.get_variables()
