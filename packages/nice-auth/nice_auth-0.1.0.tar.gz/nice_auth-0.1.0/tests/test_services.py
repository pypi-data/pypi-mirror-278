import os
import unittest
from nice_auth.services import NiceAuthService
from nice_auth.exceptions import NiceAuthException

class TestNiceAuthService(unittest.TestCase):

    def setUp(self):
        self.base_url = os.getenv("NICE_AUTH_BASE_URL")
        self.client_id = os.getenv("NICE_CLIENT_ID")
        self.client_secret = os.getenv("NICE_CLIENT_SECRET")
        self.product_id = os.getenv("NICE_PRODUCT_ID")
        self.return_url = os.getenv("NICE_RETURN_URL")
        self.authtype = os.getenv("NICE_AUTHTYPE")
        self.popupyn = os.getenv("NICE_POPUPYN")

        self.service = NiceAuthService(
            client_id=self.client_id,
            client_secret=self.client_secret,
            product_id=self.product_id,
            return_url=self.return_url,
            base_url=self.base_url,
            authtype=self.authtype,
            popupyn=self.popupyn
        )

    def test_get_token(self):
        print("Testing get_token...")
        try:
            access_token = self.service.get_token()
            print(f"Access Token: {access_token}")
            self.assertTrue(len(access_token) > 0)
        except NiceAuthException as e:
            self.fail(f"get_token raised an exception: {e}")

    def test_get_encrypted_token(self):
        print("Testing get_encrypted_token...")
        try:
            encrypted_token_data, req_dtim, req_no = self.service.get_encrypted_token()
            print(f"Encrypted Token Data: {encrypted_token_data}")
            self.assertIn("token_val", encrypted_token_data)
            self.assertIn("token_version_id", encrypted_token_data)
        except NiceAuthException as e:
            self.fail(f"get_encrypted_token raised an exception: {e}")

    def test_generate_keys(self):
        print("Testing generate_keys...")
        try:
            key, iv, hmac_key, token_version_id, token_val, site_code, req_dtim, req_no = self.service.generate_keys()
            print(f"Key: {key}, IV: {iv}, HMAC Key: {hmac_key}, Token Version ID: {token_version_id}, Site Code: {site_code}, Request Dtim: {req_dtim}, Request No: {req_no}")
            self.assertTrue(len(key) == 16)
            self.assertTrue(len(iv) == 16)
            self.assertTrue(len(hmac_key) == 32)
        except NiceAuthException as e:
            self.fail(f"generate_keys raised an exception: {e}")

    def test_get_nice_auth(self):
        print("Testing get_nice_auth...")
        try:
            auth_data = self.service.get_nice_auth()
            print(f"Auth Data: {auth_data}")
            self.assertIn("requestno", auth_data)
            self.assertIn("token_version_id", auth_data)
            self.assertIn("enc_data", auth_data)
            self.assertIn("integrity_value", auth_data)
        except NiceAuthException as e:
            self.fail(f"get_nice_auth raised an exception: {e}")

    def test_get_nice_auth_url(self):
        print("Testing get_nice_auth_url...")
        try:
            nice_url = self.service.get_nice_auth_url()
            print(f"NICE Auth URL: {nice_url}")
            self.assertTrue(nice_url.startswith("https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service"))
        except NiceAuthException as e:
            self.fail(f"get_nice_auth_url raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
