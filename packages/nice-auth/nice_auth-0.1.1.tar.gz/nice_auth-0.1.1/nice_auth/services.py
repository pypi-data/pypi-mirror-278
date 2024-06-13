import json
import base64
import requests
from datetime import datetime
from hashlib import sha256
from .exceptions import NiceAuthException
from .utils import generate_request_no, encrypt_aes, hmac_sha256, decrypt_aes


class NiceAuthService:
    def __init__(self, base_url, client_id, client_secret, product_id, return_url, authtype, popupyn):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.product_id = product_id
        self.return_url = return_url
        self.authtype = authtype
        self.popupyn = popupyn

    def get_token(self):
        url = f"{self.base_url}/digital/niceid/oauth/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }
        payload = {
            "grant_type": "client_credentials",
            "scope": "default"
        }
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()
        if response.status_code != 200 or response_json['dataHeader']['GW_RSLT_CD'] != '1200':
            error_message = response_json['dataHeader']['GW_RSLT_MSG']
            raise NiceAuthException(f"Failed to fetch token: {error_message}")
        return response_json["dataBody"]["access_token"]

    def get_encrypted_token(self):

        access_token = self.get_token()

        url = f"{self.base_url}/digital/niceid/api/v1.0/common/crypto/token"
        current_timestamp = int(datetime.now().timestamp())
        authorization_value = f"{access_token}:{current_timestamp}:{self.client_id}"
        headers = {
            "Authorization": "bearer " + base64.b64encode(authorization_value.encode()).decode(),
            "Content-Type": "application/json",
            "client_id": self.client_id,
            "ProductID": self.product_id
        }

        req_dtim = datetime.now().strftime("%Y%m%d%H%M%S")
        req_no = generate_request_no()

        payload = {
            "dataHeader": {
                "CNTY_CD": "ko"
            },
            "dataBody": {
                "req_dtim": req_dtim,
                "req_no": req_no,
                "enc_mode": "1"
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        if response.status_code != 200 or response_json['dataHeader']['GW_RSLT_CD'] != '1200':
            error_message = response_json['dataHeader']['GW_RSLT_MSG']
            raise NiceAuthException(f"Failed to fetch encrypted token: {error_message}")
        return response_json["dataBody"], req_dtim, req_no

    def generate_keys(self):
        encrypted_token_data, req_dtim, req_no = self.get_encrypted_token()
        token_val = encrypted_token_data['token_val']
        token_version_id = encrypted_token_data['token_version_id']
        site_code = encrypted_token_data['site_code']

        # Combine the values as described
        combined_string = req_dtim.strip() + req_no.strip() + token_val.strip()
        hash_value = sha256(combined_string.encode()).digest()
        base64_encoded = base64.b64encode(hash_value).decode()

        key = base64_encoded[:16]  # First 16 bytes for the key
        iv = base64_encoded[-16:]  # Last 16 bytes for the IV
        hmac_key = base64_encoded[:32]  # First 32 bytes for the HMAC key

        return key, iv, hmac_key, token_version_id, token_val, site_code, req_dtim, req_no

    def get_nice_auth(self):
        key, iv, hmac_key, token_version_id, token_val, site_code, req_dtim, req_no = self.generate_keys()

        req_data = {
            "requestno": req_no,
            "returnurl": self.return_url,
            "sitecode": site_code,
            "authtype": self.authtype,
            "popupyn": self.popupyn,
        }
        enc_data = encrypt_aes(req_data, key, iv)
        integrity_value = hmac_sha256(hmac_key, enc_data)

        return {
            "key": key,
            "iv": iv,
            "requestno": req_data["requestno"],
            "token_version_id": token_version_id,
            "enc_data": enc_data,
            "integrity_value": integrity_value
        }

    def get_nice_auth_url(self):
        auth_data = self.get_nice_auth()
        nice_url = f"https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service&token_version_id={auth_data['token_version_id']}&enc_data={auth_data['enc_data']}&integrity_value={auth_data['integrity_value']}"
        return nice_url

    def verify_auth_result(self, enc_data, key, iv):
        decrypted_data = decrypt_aes(enc_data, key, iv)
        return json.loads(decrypted_data)
