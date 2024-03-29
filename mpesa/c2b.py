import requests

from mpesa.auth import MpesaAuth, BearerTokenAuth


class C2B(MpesaAuth):
    def __init__(self):
        super(C2B, self).__init__()
        self.obtain_auth_token()

    def register(self, response_type=None, short_code=None, validation_url=None, confirmation_url=None):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.
           **Args:**
               - shortcode (str): The short code of the organization. options: Cancelled, Completed
               - response_type (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.
               - confirmation_url (str): Confirmation URL for the client.
               - validation_url (str): Validation URL for the client.
           **Returns:**
               - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
               - ConversationID (str): The unique request ID returned by mpesa for each request made
               - ResponseDescription (str): Response Description message
        """

        payload = {
            "ShortCode": short_code,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }

        headers = {
            'Content-Type': 'application/json'
        }

        resource_url = "{0}{1}".format(self._base_url, "/mpesa/c2b/v1/registerurl")
        req = requests.post(url=resource_url, headers=headers, auth=BearerTokenAuth(self._access_token), json=payload)

        return req.json()

    def simulate_c2b(self, short_code=None, command_id=None, amount=None, phone_number=None, bill_ref_no=None):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.
            **Args:**
                - short_code (str): The short code of the organization.
                - command_id (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.
                - amount (str): The amount being transacted
                - phone_number (str): Phone number (msisdn) initiating the transaction MSISDN(12 digits)
                - bill_ref_no: Optional Represents account_no
            **Returns:**
                - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                - ConversationID (str): The unique request ID returned by mpesa for each request made
                - ResponseDescription (str): Response Description message
        """

        endpoint = "/mpesa/c2b/v1/simulate"

        url = "{0}{1}".format(self._base_url, endpoint)
        headers = {
            "Content-Type": 'application/json'
        }

        payload = {
            "ShortCode": short_code,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": phone_number,
            "BillRefNumber": bill_ref_no
        }

        req = requests.post(url=url, headers=headers, auth=BearerTokenAuth(self._access_token), json=payload)

        return req.json()

