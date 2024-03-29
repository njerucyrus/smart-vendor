import base64
import datetime

from mpesa.auth import MpesaAuth


class MpesaExpress(MpesaAuth):
    def __init__(self):
        super(MpesaExpress, self).__init__()
        self.obtain_auth_token()

    def stk_push(
            self,
            amount=None,
            callback_url=None,
            reference_code="test_account",
            phone_number=None,
            description=None
    ):
        """This method uses Mpesa's Express API to initiate online payment on behalf of a customer..

                                                    **Args:**
                                                        - business_shortcode (str): The short code of the organization.
                                                        - lnm_passkey (str): Get from developer portal
                                                        - amount (str): The amount being transacted
                                                        - callback_url (str): A CallBack URL is a valid secure URL that is used to receive notifications from M-Pesa API.
                                                        - reference_code: Account Reference: This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type.
                                                        - phone_number: The Mobile Number to receive the STK Pin Prompt.
                                                        - description: This is any additional information/comment that can be sent along with the request from your system. MAX 13 characters


                                                    **Returns:**
                                                        - CustomerMessage (str):
                                                        - CheckoutRequestID (str):
                                                        - ResponseDescription (str):
                                                        - MerchantRequestID (str):
                                                        - ResponseCode (str):

        """

        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")
        password = "{0}{1}{2}".format(str(self._short_code), self._lnm_passkey, time)
        encoded = base64.b64encode(bytes(password, "utf-8"))
        payload = {
            "BusinessShortCode": self._short_code,
            "Password": str(encoded, "utf-8"),
            "Timestamp": time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(amount),
            "PartyA": str(phone_number),
            "PartyB": str(self._short_code),
            "PhoneNumber": str(phone_number),
            "CallBackURL": callback_url,
            "AccountReference": reference_code,
            "TransactionDesc": description
        }
        headers = {'Authorization': 'Bearer {0}'.format(self._access_token), 'Content-Type': "application/json"}

        print(f"payload: {payload}")

        url = "{0}{1}".format(self._base_url, "/mpesa/stkpush/v1/processrequest")

        r = self.session.post(url=url, headers=headers, json=payload)
        return r.json()

    def query(self, business_shortcode=None, checkout_request_id=None, lnm_passkey=None):
        """This method uses Mpesa's Express API to check the status of a Lipa Na M-Pesa Online Payment..

                                                    **Args:**
                                                        - business_shortcode (str): This is organizations shortcode (Paybill or Buygoods - A 5 to 6 digit account number) used to identify an organization and receive the transaction.
                                                        - checkout_request_id (str): This is a global unique identifier of the processed checkout transaction request.
                                                        - lnm_passkey (str): Get from developer portal


                                                    **Returns:**
                                                        - CustomerMessage (str):
                                                        - CheckoutRequestID (str):
                                                        - ResponseDescription (str):
                                                        - MerchantRequestID (str):
                                                        - ResponseCode (str):
        """

        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")
        password = "{0}{1}{2}".format(str(business_shortcode), str(lnm_passkey), time)
        encoded = base64.b64encode(bytes(password, "utf-8"))
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": str(encoded, "utf-8"),
            "Timestamp": time,
            "CheckoutRequestID": checkout_request_id
        }
        headers = {'Authorization': 'Bearer {0}'.format(self._access_token), 'Content-Type': "application/json"}

        url = "{0}{1}".format(self._base_url, "/mpesa/stkpushquery/v1/query")
        r = self.session.post(url=url, headers=headers, json=payload)
        return r.json()
