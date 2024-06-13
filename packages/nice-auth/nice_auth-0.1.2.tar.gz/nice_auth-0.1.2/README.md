# python-nice-auth

A Python library for NICE authentication.

**Current version: 0.1.2**

## Overview

`python-nice-auth` is a Python library that provides an interface for interacting with the NICE authentication API. It supports obtaining tokens, generating encrypted tokens, and creating URLs for NICE authentication services.

## Installation

To install the library, use pip:

```bash
pip install python-nice-auth
```

## Configuration

Before using the library, you need to set up the necessary configuration values. Add the following environment variables to your .env file or set them directly in your environment:

```env
NICE_AUTH_BASE_URL=https://svc.niceapi.co.kr:22001
NICE_CLIENT_ID=your_client_id
NICE_CLIENT_SECRET=your_client_secret
NICE_PRODUCT_ID=your_product_id
NICE_RETURN_URL=your_return_url
NICE_AUTHTYPE=M
NICE_POPUPYN=N
```

## Usage

### Initializing the Service

First, you need to initialize the NiceAuthService with the necessary configuration values:

```python
from nice_auth.services import NiceAuthService

# Initialize the service with configuration values
nice_auth_service = NiceAuthService(
    base_url="https://nice.checkplus.co.kr",
    client_id="your_client_id",
    client_secret="your_client_secret",
    product_id="your_product_id",
    return_url="your_return_url",
    authtype="your_authtype",
    popupyn="your_popupyn"
)
```

### Getting a Token

You can obtain a token by calling the get_token method:

```python
access_token = nice_auth_service.get_token()
```


### Getting an Encrypted Token

To get an encrypted token, use the get_encrypted_token method:

```python
encrypted_token_data, req_dtim, req_no = nice_auth_service.get_encrypted_token(access_token)
```


### Getting NICE Auth Data
To get the necessary data for NICE authentication, use the get_nice_auth method:

```python
auth_data = nice_auth_service.get_nice_auth()
```


### Generating NICE Auth URL
Finally, you can generate the NICE authentication URL:

```python
nice_auth_url = nice_auth_service.get_nice_auth_url()
```

### Verifying Authentication Result
To verify the authentication result, use the verify_auth_result method:

```python
auth_result = nice_auth_service.verify_auth_result(enc_data, key, iv)
```

### Complete Example
Here is a complete example of using the library:

```python
from nice_auth.services import NiceAuthService

# Initialize the service with configuration values
nice_auth_service = NiceAuthService(
    base_url="https://nice.checkplus.co.kr",
    client_id="your_client_id",
    client_secret="your_client_secret",
    product_id="your_product_id",
    return_url="your_return_url",
    authtype="your_authtype",
    popupyn="your_popupyn"
)

# Get a token
access_token = nice_auth_service.get_token()

# Get an encrypted token
encrypted_token_data, req_dtim, req_no = nice_auth_service.get_encrypted_token(access_token)

# Generate NICE Auth URL
nice_auth_url = nice_auth_service.get_nice_auth_url()
print(f"NICE Auth URL: {nice_auth_url}")
```

## License
This project is licensed under the MIT License.

