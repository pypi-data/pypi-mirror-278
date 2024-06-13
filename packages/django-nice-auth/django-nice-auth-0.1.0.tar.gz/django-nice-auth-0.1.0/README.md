# Django NiceAuth Library

A Django library for integrating NICE authentication services. This library provides an interface for generating authentication data, retrieving authentication URLs, and verifying authentication results.

## Overview

`django-niceauth` is a Django library that provides an interface for interacting with the NICE authentication API. It supports obtaining tokens, generating encrypted tokens, and creating URLs for NICE authentication services.

## Requirements

- Python 3.6+
- Django 3.0+
- `nice_auth` library

## Installation

1. **Install the library:**

    ```bash
    pip install django-niceauth
    ```

2. **Add the library to your Django project:**

    Add `'niceauth'` to your `INSTALLED_APPS` in the Django settings file.

    ```python
    INSTALLED_APPS = [
        ...
        'niceauth',
    ]
    ```

3. **Set up your environment variables:**

    Create a `.env` file in the root directory and add the following configurations:

    ```env
    NICE_AUTH_BASE_URL=https://svc.niceapi.co.kr:22001
    NICE_CLIENT_ID=your_client_id
    NICE_CLIENT_SECRET=your_client_secret
    NICE_PRODUCT_ID=your_product_id
    NICE_RETURN_URL=https://yourdomain.com/verify
    NICE_AUTHTYPE=M
    NICE_POPUPYN=N
    ```

4. **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

## Configuration

Before using the library, you need to set up the necessary configuration values in your `.env` file as shown above.

## Usage

### Models

The library includes the following models to store authentication requests and results:

- `NiceAuthRequest`: Stores the request data.
- `NiceAuthResult`: Stores the result data.

### API Endpoints

The library provides the following API endpoints:

1. **Get NICE Authentication Data**

    - **URL:** `/api/niceauth/data/`
    - **Method:** `POST`
    - **Response:**

        ```json
        {
            "request_no": "REQUEST_NO",
            "enc_data": "ENCRYPTED_DATA",
            "integrity_value": "INTEGRITY_VALUE",
            "token_version_id": "TOKEN_VERSION_ID"
        }
        ```

2. **Get NICE Authentication URL**

    - **URL:** `/api/niceauth/url/`
    - **Method:** `POST`
    - **Response:**

        ```json
        {
            "nice_auth_url": "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service&token_version_id=TOKEN_VERSION_ID&enc_data=ENCRYPTED_DATA&integrity_value=INTEGRITY_VALUE"
        }
        ```

3. **Verify NICE Authentication Result**

    - **URL:** `/api/niceauth/verify/`
    - **Method:** `POST`
    - **Request Body:**

        ```json
        {
            "enc_data": "ENCRYPTED_DATA",
            "token_version_id": "TOKEN_VERSION_ID",
            "integrity_value": "INTEGRITY_VALUE"
        }
        ```
    - **Response:**

        ```json
        {
            "resultcode": "0000",
            "requestno": "REQUEST_NO",
            "sitecode": "SITE_CODE",
            ...
        }
        ```

### Example Usage

#### Initializing the Service

First, you need to initialize the `NiceAuthService` with the necessary configuration values:

```python
from nice_auth.services import NiceAuthService

service = NiceAuthService(
    base_url=settings.NICE_AUTH_BASE_URL,
    client_id=settings.NICE_CLIENT_ID,
    client_secret=settings.NICE_CLIENT_SECRET,
    product_id=settings.NICE_PRODUCT_ID,
    return_url=settings.NICE_RETURN_URL,
    authtype=settings.NICE_AUTHTYPE,
    popupyn=settings.NICE_POPUPYN
)

### Getting NICE Authentication Data

```python
auth_data = service.get_nice_auth()
```

### Getting NICE Authentication URL

```python
nice_url = service.get_nice_auth_url()
```

### Verifying NICE Authentication Result

```python
result_data = service.verify_auth_result(enc_data, key, iv)
```

## Running Tests
To run the tests, use the following command:

```bash
python manage.py test
```