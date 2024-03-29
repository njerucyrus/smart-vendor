import os
from base64 import b64encode

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from dotenv import load_dotenv
from requests.auth import AuthBase, HTTPBasicAuth

from mpesa.session import RequestSession

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BearerTokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


class MpesaAuth(RequestSession):
    def __init__(self):
        super().__init__()
        self._env = os.environ.get("MPESA_ENV")
        self._consumer_key = os.environ.get("MPESA_CONSUMER")
        self._secret_key = os.environ.get('MPESA_SECRET')
        self._lnm_passkey = os.environ.get('MPESA_LNM_PASSKEY')
        self._short_code = os.environ.get("MPESA_SHORT_CODE")
        self._access_token = None
        self._initiator_password = None

        if self._env == "sandbox":

            self._base_url = "https://sandbox.safaricom.co.ke"
            self.cert_path = os.path.join(BASE_DIR, 'mpesa/mpesa_sandbox_cert.cer')

        elif self._env == "live":
            self.cert_path = os.path.join(BASE_DIR, 'mpesa/mpesa_prod_cert.cer')
            self._base_url = "https://api.safaricom.co.ke"

        else:
            self._base_url = None

    def obtain_auth_token(self):
        """To make Mpesa API calls, you will need to authenticate your app. This method is used to fetch the access token
               required by Mpesa. Mpesa supports client_credentials grant type. To authorize your API calls to Mpesa,
               you will need a Basic Auth over HTTPS authorization token. The Basic Auth string is a base64 encoded string
               of your app's client key and client secret.

           **Args:**
               - env (str): Current app environment. Options: sandbox, live.
               - app_key (str): The app key obtained from the developer portal.
               - app_secret (str): The app key obtained from the developer portal.

           **Returns:**
               - access_token (str): This token is to be used with the Bearer header for further API calls to Mpesa.
        """

        auth_endpoint = "/oauth/v1/generate?grant_type=client_credentials"

        url = "{0}{1}".format(self._base_url, auth_endpoint)

        req = self.session.get(url=url, auth=HTTPBasicAuth(self._consumer_key, self._secret_key))
        print(req.json())
        if req.status_code == 200:
            self._access_token = req.json()['access_token']
            return self._access_token
        else:
            self._access_token = None
            return self._access_token

    def security_credential(self):
        """
        old version of code works with M2Crypto Library which has some problems installing

        cert_file = open(self.cert_path, 'rb')
        cert_data = cert_file.read()  # read certificate file
        cert_file.close()

        cert = X509.load_cert_string(cert_data)
        # pub_key = X509.load_cert_string(cert_data)
        pub_key = cert.get_pubkey()
        rsa_key = pub_key.get_rsa()
        cipher = rsa_key.public_encrypt(bytes(str(self.initiator_password), "utf-8"), RSA.pkcs1_padding)
        return b64encode(cipher)

        """
        with open(self.cert_path, "rb") as cert_file:
            cert_data = cert_file.read()

        # Load the certificate from the data
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # Get the public key from the certificate
        pub_key = cert.public_key()

        # If the public key is an RSA key, we can use it for encryption
        if isinstance(pub_key, rsa.RSAPublicKey):
            # Encrypt the password using the RSA public key
            cipher = pub_key.encrypt(
                bytes(str(self._initiator_password), "utf-8"),
                padding.PKCS1v15()
            )
            return b64encode(cipher)
        else:
            # Handle the case where the public key is not RSA
            raise ValueError("Public key is not an RSA key")
