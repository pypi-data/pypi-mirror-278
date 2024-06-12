# LicenseSpring Python Library

The LicenseSpring Python Library provides convenient access to the LicenseSpring API from
applications written in the Python language.

## Installation

Install `licensespring` library:

```
pip install licensespring
```

Requires: Python >=3.7

## Hardware (Device) IDs

This library provides preconfigured hardware identity providers:
- `HardwareIdProvider` (default)
- `PlatformIdProvider`

You can set the desired hardware identity provider when initializing the APIClient:
```python
from licensespring.hardware import PlatformIdProvider

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_", hardware_id_provider=PlatformIdProvider)
```

It also supports their customization and creation of your own hardware id provider.

### HardwareIdProvider

Uses [uuid.getnode()](https://docs.python.org/3/library/uuid.html#uuid.getnode) to generate unique ID per device as described:

> Get the hardware address as a 48-bit positive integer. The first time this runs, it may launch a separate program, which could be quite slow. If all attempts to obtain the hardware address fail, we choose a random 48-bit number with the multicast bit (least significant bit of the first octet) set to 1 as recommended in RFC 4122. “Hardware address” means the MAC address of a network interface. On a machine with multiple network interfaces, universally administered MAC addresses (i.e. where the second least significant bit of the first octet is unset) will be preferred over locally administered MAC addresses, but with no other ordering guarantees.

All of the methods exposed by `HardwareIdProvider`:
```python
class HardwareIdProvider:
    def get_id(self):
        return str(uuid.getnode())

    def get_os_ver(self):
        return platform.platform()

    def get_hostname(self):
        return platform.node()

    def get_ip(self):
        return socket.gethostbyname(self.get_hostname())

    def get_is_vm(self):
        return False

    def get_vm_info(self):
        return None

    def get_mac_address(self):
        return ":".join(("%012X" % uuid.getnode())[i : i + 2] for i in range(0, 12, 2))

    def get_request_id(self):
        return str(uuid.uuid4())
```

### PlatformIdProvider

Uses [sys.platform](https://docs.python.org/3/library/sys.html#sys.platform) and OS queries to find the raw GUID of the device.

Extends the `HardwareIdProvider` and overwrites only the `get_id` method:
```python
class PlatformIdProvider(HardwareIdProvider):
    def get_id(self):
        id = None

        if sys.platform == 'darwin':
            id = execute("ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'")

        if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':
            id = read_win_registry('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography', 'MachineGuid')
            if not id:
                id = execute('wmic csproduct get uuid').split('\n')[2].strip()

        if sys.platform.startswith('linux'):
            id = read_file('/var/lib/dbus/machine-id')
            if not id:
                id = read_file('/etc/machine-id')

        if sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
            id = read_file('/etc/hostid')
            if not id:
                id = execute('kenv -q smbios.system.uuid')

        if not id:
            id = super().get_id()

        return id
```

### Customization

Extend any of the preconfigured hardware identity providers, overwrite the methods you want and provide it when initializing the APIClient:
```python
class CustomHardwareIdProvider(HardwareIdProvider):
    def get_id(self):
        return "_my_id_"

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_", hardware_id_provider=CustomHardwareIdProvider)
```

## APIClient Usage Examples

### Set app version
```python
import licensespring

licensespring.app_version = "MyApp 1.0.0"
```

### Create APIClient
```python
from licensespring.api import APIClient

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")
```

### Activate key based license
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"
license_data = api_client.activate_license(product=product, license_key=license_key)

print(license_data)
```

### Activate user based license
```python
product = "uprod1"
username = "user1@email.com"
password = "nq64k1!@"

license_data = api_client.activate_license(
    product=product, username=username, password=password
)

print(license_data)
```

### Deactivate key based license
```python
product = "lkprod1"
license_key = "GPUB-J4PH-CGNK-C7LK"
api_client.deactivate_license(product=product, license_key=license_key)
```

### Deactivate user based license
```python
product = "uprod1"
username = "user1@email.com"

api_client.deactivate_license(
    product=product, username=username
)
```

### Check key based license
```python
product = "lkprod1"
license_key = "GPBQ-DZCP-E9SK-CQLK"

license_data = api_client.check_license(product=product, license_key=license_key)

print(license_data)
```

### Check user based license
```python
product = "uprod1"
username = "user2@email.com"
password = "1l48y#!b"

license_data = api_client.check_license(product=product, username=username)

print(license_data)
```

### Add consumption
```python
product = "lkprod1"
license_key = "GPSU-QTKQ-HSSK-C9LK"

# Add 1 consumption
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key
)

print(consumption_data)

# Add 3 consumptions
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, consumptions=3
)

print(consumption_data)

# Add 1 consumption, allow overages and define max overages
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, allow_overages=True, max_overages=10
)

print(consumption_data)
```

### Add feature consumption
```python
product = "lkprod1"
license_key = "GPTJ-LSYZ-USEK-C8LK"
feature = "lkprod1cf1"

# Add 1 consumption
feature_consumption_data = api_client.add_feature_consumption(
    product=product, license_key=license_key, feature=feature
)

# Add 3 consumptions
feature_consumption_data = api_client.add_feature_consumption(
    product=product, license_key=license_key, feature=feature, consumptions=3
)

print(feature_consumption_data)
```

### Trial key
```python
product = "lkprod2"

trial_license_data = api_client.trial_key(product=product)

print(trial_license_data)
```

### Product details
```python
product = "lkprod1"

product_data = api_client.product_details(product=product)

print(product_data)
```

### Track device variables
```python
product = "lkprod1"
license_key = "GPUB-SZF9-AB2K-C7LK"
variables = {"variable_1_key": "variable_1_value", "variable_2_key": "variable_2_value"}

device_variables = api_client.track_device_variables(product=product, license_key=license_key, variables=variables)

print(device_variables)
```

### Get device variables
```python
product = "lkprod1"
license_key = "GPUB-SZF9-AB2K-C7LK"

device_variables = api_client.get_device_variables(product=product, license_key=license_key)

print(device_variables)
```

### Floating borrow
```python
product = "lkprod1"
license_key = "GPUC-NGWU-3NJK-C7LK"

# Borrow for 2 hours
borrowed_until = (datetime.utcnow() + timedelta(hours=2)).isoformat()
floating_borrow_data = api_client.floating_borrow(product=product, license_key=license_key, borrowed_until=borrowed_until)

print(floating_borrow_data)
```

### Floating release
```python
product = "lkprod1"
license_key = "GPUC-NGWU-3NJK-C7LK"

api_client.floating_release(product=product, license_key=license_key)
```

### Change password
```python
username = "user4@email.com"
password = "_old_password_"
new_password = "_new_password_"

is_password_changed = api_client.change_password(username=username, password=password, new_password=new_password)

print(is_password_changed)
```

### Versions
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"

# Get versions for all environments
versions_data = api_client.versions(product=product, license_key=license_key)

# Get versions for mac environment
mac_versions_data = api_client.versions(
    product=product, license_key=license_key, env="mac"
)

print(versions_data)
```

### Installation file
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"

# Get the latest installation file
installation_file_data = api_client.installation_file(
    product=product, license_key=license_key
)

# Get the latest installation file for linux environment
installation_file_data = api_client.installation_file(
    product=product, license_key=license_key, env="linux"
)

# Get the latest installation file for version 1.0.0
installation_file_data = api_client.installation_file(
    product=product, license_key=license_key, version="1.0.0"
)

print(installation_file_data)
```

### Customer license users
```python
product = "uprod1"
customer = 'c1@c.com'

customer_license_users_data = api_client.customer_license_users(
    product=product, customer=customer
)

print(customer_license_users_data)
```

### SSO URL
```python
product = "uprod1"
customer_account_code = "ccorp"

sso_url_data = api_client.sso_url(
    product=product, customer_account_code=customer_account_code
)

print(sso_url_data)
```


### SSO URL with `code` response type
```python
product = "uprod1"
customer_account_code = "ccorp"

sso_url_data = api_client.sso_url(
    product=product,
    customer_account_code=customer_account_code,
    response_type="code",
)

print(sso_url_data)
```

### Activate offline
```python
product = "lkprod1"
license_key = "GPY7-VHX9-MDSK-C3LK"

# Generate data for offline activation
activate_offline_data = api_client.activate_offline_dump(
    product=product, license_key=license_key
)

# Write to file
with open('activate_offline.req', mode='w') as f:
    print(activate_offline_data, file=f)

# Activate offline
license_data = api_client.activate_offline(data=activate_offline_data)

print(license_data)
```

### Activate offline load
```python
# Read from file
with open('./ls_activation.lic') as file:
    ls_activation_data = file.read()

license_data = api_client.activate_offline_load(ls_activation_data)

print(license_data)
```

### Check offline load
```python
# Read from file
with open('./license_refresh.lic') as file:
    license_refresh_data = file.read()

license_data = api_client.check_offline_load(license_refresh_data)

print(license_data)
```


### Deactivate offline
```python
product = "lkprod1"
license_key = "GPYC-X5J2-L5SK-C3LK"

# Generate data for offline deactivation
deactivate_offline_data = api_client.deactivate_offline_dump(
    product=product, license_key=license_key
)

# Write to file
with open('deactivate_offline.req', mode='w') as f:
    print(deactivate_offline_data, file=f)

# Deactivate offline
api_client.deactivate_offline(data=deactivate_offline_data)
```

### Key based license feature check
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"
feature = "lkprod1f1"

license_feature_data = api_client.check_license_feature(
    product=product, feature=feature, license_key=license_key
)

print(license_feature_data)
```

### Key based license floating feature release
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"
feature = "lkprod1f1"

api_client.floating_feature_release(
    product=product, feature=feature, license_key=license_key
)
```

## Licensefile

### Licensefile setup  
To use licensefile inside a python SDK you should first setup your key and IV. Key and IV are used inside Python SDK for encryption and decryption process inside licensefile. For the first setup it is essenital to chose **password** and **salt** for key generation. This process is only required **once** at the setup.  
```python
from licensespring.licensefile.default_crypto import DefaultCryptoProvider

password = "YOUR_PASSWORD"
salt = "YOUR_SALT"


crypto = DefaultCryptoProvider()

key = crypto.derive_key(password=key_password,salt=key_salt)
iv = crypto.generate_random_iv()
```
### Configuration Setup
After you have successfully setup your key and IV you should setup your Configuration.
```python
from licensespring.licensefile.config import Configuration

conf = Configuration(product="your_product_short_code",
        api_key="your_api_key",
        shared_key="your_shared_key",
        file_key=key,
        file_iv=iv,
        hardware_id_provider=HardwareIdProvider,
        verify_license_signature=True,
        signature_verifier=SignatureVerifier,
        api_domain="api.licensespring.com",
        api_version="v4",
        filename="License",
        file_path=None,
        grace_period_conf=24)
```

* **product (str)**: product short code.    
* **api_key (str)**: Your unique API key used for authentication with the licensing server.   
* **shared_key (str)**: A shared secret key used alongside the API key for enhanced security during the license verification process.  
* **file_key (str)**: The encryption key used for securing license files on the client side.   
* **file_iv (str)**: The initialization vector for the encryption algorithm. This complements the file_key for encrypting and decrypting license files.   
* **hardware_id_provider (object, optional)**: The provider class used for generating a unique hardware ID. This ID helps in binding the license to specific hardware. Defaults to HardwareIdProvider.  
* **verify_license_signature (bool, optional)**: A boolean flag indicating whether the license's digital signature should be verified. Defaults to True for enhanced security.  
* **signature_verifier (object, optional)**: The class responsible for verifying the digital signature of licenses. Defaults to SignatureVerifier.  
* **api_domain (str, optional)**: The domain name of the API server with which the licensing operations are performed. Defaults to "api.licensespring.com".  
* **api_version (str, optional)**: The version of the API to use for requests. This allows for compatibility with different versions of the licensing API. Defaults to "v4".  
* **filename (str, optional)**: The default filename for saved license files. This can be customized as needed. Defaults to "License".  
* **file_path (str, optional)**: The path where license files should be saved on the client system. If not specified, a **[default location](https://docs.licensespring.com/sdks/tutorials/best-practices/local-license-file#W8U6X)** is used.  
* **grace_period_conf (int, optional)**: The number of hours to allow as a grace period for  Defaults to 24 hours.  

### LicenseID

* **from_key(cls, key)**: Class method to create a LicenseID instance for key-based activation  
* **from_user(cls, username, password)**: Class method to create a LicenseID instance for user-based activation.

#### Key-based setup
```python
license_id = LicenseID.from_key("your_license_key") 
```
#### User-based setup
```python
license_id = LicenseID.from_user(username="email@email.com",password="password")                          
```
### LicenseManager  
```python
from licensespring.licensefile.license_manager import LicenseManager,LicenseID

manager = LicenseManager(conf)
```
#### Configuration parametres

conf (Configuration): **[A configuration object](#configuration-setup)**

#### activate_license
Activates a license with the license server and updates local license data.

**Key-based**
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H6QM-6H5R-ZENJ-VBLK")

license = manager.activate_license(license_id)
```
**User-based**
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_user(username="python@gmail.com",password="7t_x3!o9")

license = manager.activate_license(license_id)
```
**Parameters**:  
* **license_id** (LicenseID): An instance containing the license key or user credentials.    

**Return**:
**License** object representing the activated license.

#### load_license  
Loads the license file and sets attributes for the LicenseData instance. Returns an instance of the License class reflecting the loaded license.

```python
manager = LicenseManager(conf)

license = manager.load_license()
```
#### is_online  
Checks if the licensing server is accessible. Returns True if online, False otherwise.

```python
manager = LicenseManager(conf)

license = manager.is_online()
```

#### create_offline_activation_file
Creates .req file for offline activation, including various optional parameters related to the device and software environment. 

**Parameters**:

* **license_id** (LicenseID): An instance containing the license key or user credentials.  
* **req_path** (str): Specify the path where to create .req file.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H94R-S6KB-L7AJ-SXLK")

req_file_path = manager.create_offline_activation_file(license_id,'offline_files/test')              
```
**Return** (str): Path of the .req file created for activation.

#### activate_license_offline
Activates a license offline using a .lic file provided via the specified path.

**Parameters**:

* **ls_activation_path** (str): Path to the activation file.

```python
file_path = 'offline_files/ls_activation.lic'

manager = LicenseManager(conf)

license = manager.activate_license_offline(file_path)
```
**Raises**:

* **LicenseActivationException**: Activation data is not valid.
* **LicenseActivationException**: Response file ID mismatch.
* L**icenseActivationException**: License does not belong to this device.

**Return**(License): Returns a License object representing the activated license.

#### get_trial_license
Creates LiceseID for trial licenses

**Parameters**:

* **customer** (Customer): Customer object
* **license_policy** (str,optional): license policy code. Defaults to None.

```python
customer = Customer(email='python_policy@gmail.com')  

manager = LicenseManager(conf)

license_id = manager.get_trial_license(customer=customer,license_policy='test')
    
license = manager.activate_license(license_id=license_id)
```

**Return**(LicenseID): Returns a LicenseID object.

### License object

Object responsible for license operations


#### is_validity_period_expired

Determines whether the license's validity period has expired

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
license.is_validity_period_expired()                 
```
**Return (bool)**: True if license expired;False if license is valid

#### check_license_status

Verifies the current status of the license. It raises exceptions if the license is not enabled, not active, or expired

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
license.check_license_status()                                       
```
**Raises**:  
**LicenseStateException**: Raised if the license fails one of the following checks:
* License is not enabled.
* License is not active.
* License validity period has expired.  

**Return**: None

#### check

Performs an online check to synchronize the license data with the backend. This includes syncing consumptions for consumption-based licenses.

**Parameters**:

* **include_expired_features (bool, optional)**: Includes expired license features in the check.

  
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
response=license.check()                                                            
```
**Raises**:

**ClientError**: Raised if there's an issue with the API client's request, such as invalid credentials or unauthorized access.

**RequestException**: Raised if there's a problem with the request to the licensing server, such as network issues or server unavailability.

**Return (dict)**: The updated license cache.

#### deactivate

Deactivates the license and optionally deletes the local license file.

**Parameters**:

* **delete_license (bool, optional)**: If **True**, deletes the local license file upon deactivation.

  
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
license.deactivate()                                                       
```

**Return**: None


#### local_check

This method ensures the integrity and consistency of the licensing information by comparing the data stored in the local license file with the predefined configurations in the **Configuration object**.

  
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
license.local_check()                                                                      
```
**Raises**:

**ConfigurationMismatch**: Raised if the product code or hardware ID in the license file does not match the expected values provided in the Configuration  
**VMIsNotAllowedException**: Raised if the license is used in a VM environment when the license explicitly disallows it.  
**TimeoutExpiredException**: Raised if a floating license has expired. This is more relevant if is_floating_expired is later implemented to perform actual checks.
**ClockTamperedException**: Raised if there is evidence of tampering with the system's clock, detected by comparing the system's current time with the last usage time recorded in the license file.

**Return**: None

#### add_local_consumption

Adds local consumption records for **consumption-based licenses**.
**Parameters**:

* **consumptions (bool, optional)**: The number of consumptions to add locally
  
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)
    
license.add_local_consumption()           
```

**Raises**:  
**LicenseSpringTypeError**: Raised if the license type does not support consumption (i.e., not a consumption-based license).  
**ConsumptionError**: Raised if adding the specified number of consumptions would exceed the allowed maximum for the license.

**Return (dict)**: The updated license cache reflecting the new consumption count.

#### sync_consumption

Synchronizes local consumption data with the server, adjusting for overages if specified.

Parameters:
* **req_overages (int, optional)**: Specifies behavior for consumption overages.
 
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.add_local_consumption(5)
    
license.sync_consumption()
```
**Raises**:    
**RequestException**: Raised if the request to synchronize consumption data with the server fails, for instance, due to network issues or server unavailability.

Return (bool): True if the consumption data was successfully synchronized; False otherwise.

#### is_grace_period

Determines if the current license state is within its grace period following a specific exception.
 
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

boolean = license.is_grace_period()
```
**Return (bool)**: True if the license is within its grace period, False otherwise

#### change_password

Changes password of a user

**Parameters**:

* **password** (str): Old password of license user
* **new_password**(str): New password of license user

 
```python
manager = LicenseManager(conf)

license_id = LicenseID.from_user(username="python@gmail.com",password="7t_x3!o9")

license = manager.activate_license(license_id)

license.change_password(password="7t_x3!o9",new_password="12345678")                    
```
**Return (str)**: "password_changed"


#### setup_license_watch_dog

Initializes and starts the license watchdog with the specified callback and timeout settings to monitor license activity or conditions.

**Parameters**:

**callback** (Callable): A callable to be executed by the watchdog in response to specific events or conditions.  
**timeout** (int): The period in minutes after which the watchdog should perform its checks.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.setup_license_watch_dog(callback,timeout)                   
```


**Return**: None

#### stop_license_watch_dog

Stops the license watchdog if it is currently running, effectively halting its monitoring and callback activities.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.setup_license_watch_dog(callback,timeout)
                                
license.stop_license_watch_dog()                  
```
**Return**: None

#### add_local_feature_consumption
Adds local consumption to the feature.

**Parameters**:
* **feature** (str): feature code.
* **consumptions** (int,optional): Number of consumptions.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.add_local_feature_consumption("lkprod1cf1",3) 
```    

**Raises**:

* **ItemNotFoundError**: If the feature specified by `feature_code` does not exist.

* **LicenseSpringTypeError**: If the identified feature is not of the "consumption" type.

* **ConsumptionError**: If adding the specified number of consumptions would exceed the feature's consumption limits.



**Return**: None


#### sync_feature_consumption
Synchronizes local consumption data with the server.
**Parameters**:

* **feature** (str): feature code.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.add_local_feature_consumption("lkprod1cf1",3)

license.sync_feature_consumption("lkprod1cf1")
```             

**Return** (bool): True if the consumption data was successfully synchronized; False otherwise.


#### floating_borrow
Attempts to borrow a floating license until the specified date, updating the system status based on the outcome of the borrow attempt.

**Parameters**:

* **borrow_until** (str): A string representing the date until which the license should be borrowed.
* **password** (str,optional): Password for the license if required.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.floating_borrow("2031-05-06T00:00:00Z")    
```  
**Return**: None

#### floating_release
Releases a borrowed floating license and updates the license status accordingly.

**Parameters**:

* **throw_e**(bool): A boolean indicating whether to raise an exception on failure.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.check()

license.floating_release(False)   
```  

**Return**: None

#### check_feature
Checks for a specific license feature and updates the license cache accordingly.

**Parameters**:

* **feature**(str): feature code.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.check_feature("lkprod1f1fc1")    
```  

**Return**: None

#### release_feature
Releases a borrowed license feature and updates the license cache accordingly.

**Parameters**:

* **feature**(str): feature code.

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H7G3-F4PJ-4AEJ-UKYL")

license = manager.activate_license(license_id)

license.check_feature("lkprod1f1fc1")

license.release_feature("lkprod1f1fc1")   
```  

**Return**: None

#### update_offline
Updates license via refresh file

**Parameters**:

* **path** (str): path of the refresh file
* **reset_consumption** (bool): True resets consumption otherwise False


```python
file_path = 'path_to_lic_file/license.lic'

manager = LicenseManager(conf)

license = manager.activate_license_offline(file_path)

license.update_offline('offline_files/license_refresh.lic',False)                      
```  
**Raises**:

* **ConfigurationMismatch**: The update file does not belong to this device
* **ConfigurationMismatch**: The update file does not belong to this product  

**Return**(bool): True if license was successfully updated otherwise False

#### deactivate_offline
Generates .req file for the offline deactivation

**Parameters**:

* **offline_path**(str): path of the .req file


```python
file_path = 'path_to_lic_file/license.lic'

manager = LicenseManager(conf)

license = manager.activate_license_offline(file_path)

license.deactivate_offline('path_where_to_create_req_file')                     
```  
**Raises**:

* **ConfigurationMismatch**: The update file does not belong to this device
* **ConfigurationMismatch**: The update file does not belong to this product  

**Return**(bool): True if license was successfully updated otherwise False

#### product_details
Update product details from LicenseSpring server

**Parameters**:

* **include_custom_fields** (bool, optional): custom fields information. Defaults to False.
* **include_latest_version** (bool, optional): Lateset version information. Defaults to False.
            

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H9V3-72XX-ZRAJ-S6LK")

license = manager.activate_license(license_id)
    
response = license.product_details()                    
```  
**Raises**:
 

**Return**(dict): response

#### get_device_variables
Get device variable if exists

**Parameters**:

* **variable_name** (str): variable name            

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H9V3-72XX-ZRAJ-S6LK")

license = manager.activate_license(license_id)
    
device_var = license.get_device_variable('english')               
```  
**Raises**:
 

**Return**(dict): variable dictionary

#### set_device_variables
Set device variables locally 

**Parameters**:

* **variables** (dict): variables dict
* **save** (bool, optional): Save cache to licensefile. Defaults to True.
            

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H9V3-72XX-ZRAJ-S6LK")

license = manager.activate_license(license_id)
    
license.set_device_variables({"english":"value"})                   
```  
**Raises**:
 

**Return**: None

#### get_device_variables
Get device variables from server or locally

**Parameters**:

* **get_from_be** (bool, optional): If True collects data from LicenseSpring server. Defaults to True.
            

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H9V3-72XX-ZRAJ-S6LK")

license = manager.activate_license(license_id)
    
license.get_device_variables(get_from_be=True)                 
```  
**Raises**:
 * **RequestException** (Grace period not allowed)

**Return**(list): List of device variables

#### send_device_variables
Send device variables to LicenseSpring server. Handles GracePeriod
            

```python
manager = LicenseManager(conf)

license_id = LicenseID.from_key("H9V3-72XX-ZRAJ-S6LK")

license = manager.activate_license(license_id)
    
license.send_device_variables()                   
```  
**Raises**:
 * **RequestException** (Grace period not allowed)

**Return**(bool): True if new variables are sent to LicenseSpring server otherwise, False

                                
## License

Copyright (C) 2023 by Cense Data Inc., support@licensespring.com

### Dependency licenses

| Name               | Version   | License                                             | URL                                                      |
|--------------------|-----------|-----------------------------------------------------|----------------------------------------------------------|
| certifi            | 2023.7.22 | Mozilla Public License 2.0 (MPL 2.0)                | https://github.com/certifi/python-certifi                |
| charset-normalizer | 3.3.0     | MIT License                                         | https://github.com/Ousret/charset_normalizer             |
| idna               | 3.4       | BSD License                                         | https://github.com/kjd/idna                              |
| pycryptodome       | 3.19.0    | Apache Software License; BSD License; Public Domain | https://www.pycryptodome.org                             |
| requests           | 2.31.0    | Apache Software License                             | https://requests.readthedocs.io                          |
| urllib3            | 2.0.7     | MIT License                                         | https://github.com/urllib3/urllib3/blob/main/CHANGES.rst |
| winregistry        | 1.1.1     | UNKNOWN                                             | https://github.com/shpaker/winregistry                   |
