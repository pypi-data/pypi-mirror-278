"""
    rapid_client.py

    API wrapper for Axis Direct REST APIs.

    :copyright: (c) 2024 Abhay Braja.
    :license: see LICENSE for details.
"""

import json
import requests
import os
import logging

from rapidapi_axisdirect.utils import decrypt_data, encrypt_aes, encrypt_rsa

from .__version__ import __version__, __title__
from rapidapi_axisdirect import exceptions as exc

log = logging.getLogger(__name__)


class AxisAPIClient(object):
    """
    The Axis Direct API Client wrapper class.

    """

    _HANDSHAKE_ROUTE = "https://welcome-api.axisdirect.in/handshake"
    _SSO_INITIATE_ROUTE = "https://welcome-api.axisdirect.in/sso/initiate"
    _AUTHENTICATE_ROUTE = "https://welcome-api.axisdirect.in/sso/authenticate"
    _REFRESH_TOKEN_ROUTE = "https://welcome-api.axisdirect.in/v1/handshake/get-auth-token"
    _GET_PROFILE_ROUTE = "https://invest-api.axisdirect.in/customer-profile/details"
    _SECURITY_MASTER_ROUTE = "https://invest-static-assets.axisdirect.in/TELESCOPE/security_master_web/SecurityMaster.csv"
    _SEARCH_SCRIP_ROUTE = "https://invest-api.axisdirect.in/securitymaster/security-masters/{scriptId}"
    _MARGIN_ROUTE = "https://funds-api.axisdirect.in/funds/inquiry/get-limits"
    _MARGIN_REQUIRED_ROUTE = "https://funds-api.axisdirect.in/funds/inquiry/get-limits"
    _BROKERAGE_ROUTE = "https://funds-api.axisdirect.in/funds/inquiry/get-order-brokerage"
    _ORDER_PLACE_ROUTE = "https://invest-api.axisdirect.in/trading/orders/place-order"
    _ORDER_MODIFY_ROUTE = "https://invest-api.axisdirect.in/trading/orders/modify-order"
    _ORDER_CANCEL_ROUTE = "https://invest-api.axisdirect.in/trading/orders/cancel-order"
    _MARKET_STATUS_ROUTE = "https://invest-api.axisdirect.in/markettracking/tracking/get-market-status"
    _QUOTES_ROUTE = "https://invest-api.axisdirect.in/feedbroadcast/multi-touch-line"
    _BEST_FIVE_MD_ROUTE = "https://invest-api.axisdirect.in/feedbroadcast/best-five"
    _ORDER_BOOK_ROUTE = "https://invest-api.axisdirect.in/trading/orders/get-order-book"
    _ORDER_HISTORY_ROUTE = "https://invest-api.axisdirect.in/trading/orders/{orderID}/oms-order-id"
    _POSITIONS_ROUTE = "https://invest-api.axisdirect.in/trading/portfolio/get-positions"
    _TRADE_BOOK_ROUTE = "https://invest-api.axisdirect.in/trading/trades/get-trade-book"
    _HOLDINGS_ROUTE = "https://invest-api.axisdirect.in/trading/portfolio/get-holdings"
    _HOLDINGS_SUMMARY_ROUTE = "https://invest-api.axisdirect.in/trading/portfolio/get-holdings-summary"

    def __init__(self, client_id, authorization_key, debug=False):
        """
        Initialise a new Axis Direct API client instance.

        - `client_id` and `authorization_key` are the keys issued to you by the Axisdirect API Gateway.
        """
        self.AXIS_API_CLIENT_ID = client_id
        self.AXIS_AUTHORIZATION_KEY = authorization_key

        self.payload = {}
        self.session = requests.Session()
        self.message = ""

        secret_key = os.urandom(16)
        self.secret_key = secret_key.hex()
        self.sub_account_id = None  # To be set after login
        self.auth_token = None
        self.refresh_token = None

        self.debug = debug

    def set_session(self, sub_account_id, auth_token):
        """Set the `sub_account_id` and `auth_token` received after a successful authentication."""
        self.sub_account_id = sub_account_id
        self.auth_token = auth_token

    def _get_headers(self, api_encryption_key=None):
        """
            Prepare the headers for the request
        """
        headers = {
            'Content-Type': 'application/json',
            'x-api-client-id': self.AXIS_API_CLIENT_ID,
            'Authorization': self.AXIS_AUTHORIZATION_KEY,
        }
        if api_encryption_key:
            headers['x-api-encryption-key'] = api_encryption_key
        if self.sub_account_id:
            headers['x-subAccountID'] = self.sub_account_id
        if self.auth_token:
            headers['x-authtoken'] = self.auth_token
        return headers

    def _get_public_key(self):
        """
        Generate Public Key.

        """

        headers = self._get_headers()

        response = self.session.post(
            self._HANDSHAKE_ROUTE, headers=headers)

        response_data = response.json()

        if "publicKey" not in response_data['data']:
            raise exc.GeneralException(
                "`publicKey` does not exist in response")

        return response_data['data']['publicKey']

    def initiate_sso(self, redirect_URL, name="Test name"):
        """
        Initiates the SSO Login flow to get authorization url for a particular user.

        Response after decryption
        {
            "statusCode": 200,
            "status": "OK",
            "data": {
                "redirectURL": "https://auth.example.com/sso/validate?ssoId=4deefd47-cc46-4828-bc71-311f483162a4"
            }
        }
        """

        payload = {
            "type": "LOGIN",
            "redirectURL": redirect_URL,
            "metadata": {
                "name": name
            }
        }
        response = self._post(self._SSO_INITIATE_ROUTE, params=payload)
        return response

    def authenticate_sso(self, sso_id):
        """
        Generate user session details `auth_token`, `sub_account_id`, refresh_token etc by exchanging `sso_id`.
        Auth token, subAccountId and refreshToken is automatically set if the session is retrieved successfully.
        """

        payload = {
            "ssoId": sso_id
        }

        decrypted_data = self._post(
            self._AUTHENTICATE_ROUTE, params=payload)

        # Extract and store the tokens and sub_account_id
        if decrypted_data['statusCode'] == 200:
            self.sub_account_id = decrypted_data['data']['metadata']['accounts'][0]['subAccountId']
            self.auth_token = decrypted_data['data']['authToken']['token']
            self.refresh_token = decrypted_data['data']['refreshToken']['token']

        return decrypted_data['data']

    def refresh_auth_token(self, refresh_token: str):
        """
        Renew expired `auth_token` using valid `refresh_token`.

        - `refresh_token` is the token obtained from previous successful SSO Login flow.
        """

        payload = {
            "refreshToken": refresh_token
        }

        decrypted_data = self._post(
            self._REFRESH_TOKEN_ROUTE, params=payload)

        # Update the auth_token with the new one received
        if decrypted_data['statusCode'] == 200 and 'authToken' in decrypted_data['data']:
            self.auth_token = decrypted_data['data']['authToken']['token']

        return decrypted_data

    def get_profile(self):
        """Get the profile details of a logged in user."""

        if self.auth_token is None:
            raise exc.TokenException('`auth_token` should not be None. Complete login flow.')

        decrypted_data = self._get(self._GET_PROFILE_ROUTE)

        return decrypted_data

    def get_security_master(self):
        """
        Downloads the Security Master CSV file.
        """
        url = self._SECURITY_MASTER_ROUTE
        response = self.session.get(url)

        return response.status_code

    def search_scrip(self, script_id):
        """
        Searches for a scrip using the provided script ID.
        """
        url = self._SEARCH_SCRIP_ROUTE.format(scriptId=script_id)
        decrypted_data = self._get(url)
        return decrypted_data

    def available_margin(self, segment='EQ'):
        """
            Fetch the available margin in your account.
            - default segment is 'EQ'.
            - `segment` should exactly match the segment given by the security master.
        """

        payload = {
            "segment": segment
        }
        decrypted_data = self._post(self._MARGIN_ROUTE, payload)
        return decrypted_data

    def get_margin_required(self, script_id, exchange, segment, transaction_type, product_type, order_price, order_quantity, trigger_price):
        """
        Get margin required of a specific order.
        """
        payload = {
            "scriptId": script_id,
            "segment": segment,
            "exchange": exchange,
            "orderPrice": order_price,
            "orderQuantity": order_quantity,
            "transactionType": transaction_type,
            "productType": product_type,
            "triggerPrice": trigger_price,
        }
        decrypted_data = self._post(self._MARGIN_REQUIRED_ROUTE, payload)

        # headers['x-service-name'] = ''
        return decrypted_data

    def get_brokerage(self, script_id, segment, order_quantity, transaction_type, product_type, order_value):
        """
        Get estimated brokerage of an order.
        """

        payload = {
            "scriptId": script_id,
            "segment": segment,
            "orderQuantity": order_quantity,
            "orderValue": order_value,
            "productType": product_type,
            "transactionType": transaction_type,
        }
        decrypted_data = self._post(self._BROKERAGE_ROUTE, payload)

        return decrypted_data

    def place_order(self, order_ref_id,
                    script_id,
                    exchange,
                    transaction_type,
                    quantity,
                    segment,
                    order_type,
                    order_price=0,
                    disclosed_quantity=0,
                    validity_days=None,
                    product_type='DELIVERY',
                    validity_type="DAY",
                    trigger_price='0',
                    is_amo=False):
        """
        Place an order using this API.

        - `order_ref_id`: Remarks Field or local order id.
        - `script_id`: ID of the script from Security Master.
        - `transaction_type`: 'BUY' or 'SELL'
        """

        payload = {
            "orderRefId": order_ref_id,
            "segment": segment,
            "exchange": exchange,
            "scriptId": script_id,
            "transactionType": transaction_type,
            "productType": product_type,
            "orderType": order_type,
            "totalQty": quantity,
            "disclosedQty": disclosed_quantity,
            "orderPrice": order_price,
            "triggerPrice": trigger_price,
            "validityType": validity_type,
            "validityDays": validity_days,
            "isAmo": is_amo,
        }
        decrypted_data = self._post(self._ORDER_PLACE_ROUTE, payload)

        return decrypted_data

    def modify_order(self,
                     oms_order_id,
                     traded_quantity,
                     oms_order_serial_number,
                     open_quantity,
                     validity_type,
                     validity_days,
                     disclosed_quantity,
                     script_id,
                     segment,
                     order_type,
                     exchange,
                     order_price,
                     transaction_type,
                     product_type,
                     trigger_price):
        """
        Modify the order.
        """
        payload = {
            "orderRefId": oms_order_id,
            "segment": segment,
            "exchange": exchange,
            "scriptId": script_id,
            "transactionType": transaction_type,
            "productType": product_type,
            "orderType": order_type,
            "disclosedQty": disclosed_quantity,
            "orderPrice": order_price,
            "triggerPrice": trigger_price,
            "validityType": validity_type,
            "validityDays": validity_days,
            "openQty": open_quantity,
            "tradedQty": traded_quantity,
            "omsOrderSerialNumber": oms_order_serial_number,
        }
        decrypted_data = self._post(self._ORDER_MODIFY_ROUTE, payload)

        return decrypted_data

    def cancel_order(self, oms_order_id, oms_order_serial_number, open_quantity, validity_type, script_id, segment, order_type, exchange, order_price, transaction_type, product_type):
        """
        Cancels the order.
        """
        payload = {
            "omsOrderId": oms_order_id,
            "segment": segment,
            "exchange": exchange,
            "scriptId": script_id,
            "transactionType": transaction_type,
            "productType": product_type,
            "orderType": order_type,
            "orderPrice": order_price,
            "validityType": validity_type,
            "openQty": open_quantity,
            "omsOrderSerialNumber": oms_order_serial_number,
        }
        decrypted_data = self._post(self._ORDER_CANCEL_ROUTE, payload)

        return decrypted_data

    def get_market_status(self):
        """
        Get the status of the market.

        Response \n
        [{
            "exchangeSegment": "NSE_EQ",
            "updatedAt": "21/03/2024 15:30:00",
            "marketStatus": "Open"
        }]
        """
        decrypted_data = self._get(self._MARKET_STATUS_ROUTE)
        return decrypted_data

    def get_quotes(self, script_ids: list):
        """
        Get market quote of multiple scrips.

        `script_ids` should be a list of strings like ["76123445","761234"]
        """

        payload = {
            "securities": [{"scriptId": script_id} for script_id in script_ids]
        }
        decrypted_data = self._post(self._QUOTES_ROUTE, payload)

        return decrypted_data

    def get_best_five_md(self, script_id: str):
        """
        Get market depth of any scrip.
        """
        payload = {
            "scriptId": script_id
        }

        decrypted_data = self._post(self._BEST_FIVE_MD_ROUTE, payload)

        return decrypted_data

    def get_order_book(self, order_status: str, segment='EQ', oms_order_id=""):
        """
        Fetch the orders placed in your account.
        - `order_status`: The order status given in the documentation, -1, 1
        """
        payload = {
            "segment": segment,
            "omsOrderId": oms_order_id,
            "orderStatus": order_status
        }
        decrypted_data = self._post(self._ORDER_BOOK_ROUTE, payload)

        return decrypted_data

    def get_order_history(self, order_id, segment='EQ'):
        """
        Fetch the order history of a particular order.
        """

        payload = {
            "segment": segment,
        }
        url = self._ORDER_HISTORY_ROUTE.format(orderId=order_id)
        decrypted_data = self._post(url, payload)

        return decrypted_data

    def get_positions(self, segment='EQ', interop=True, type='open'):
        """Get all the positions filtered by `segment`, `type` and `interop`"""

        payload = {
            "segment": segment,
            "interop": interop,
            "type": type,
        }
        decrypted_data = self._post(self._POSITIONS_ROUTE, payload)

        return decrypted_data

    def get_trade_book(self, segment: str, order_ids: list):
        """Fetch the trades done in your account"""

        payload = {
            "segment": segment,
            "orderDetails": [{"omsOrderId": oms_order_id} for oms_order_id in order_ids]
        }
        decrypted_data = self._post(self._TRADE_BOOK_ROUTE, payload)

        return decrypted_data

    def holdings(self, segment: str):
        """
        Fetch holdings
        """

        payload = {"segment": segment}

        decrypted_data = self._post(self._HOLDINGS_ROUTE, payload)

        return decrypted_data

    def holdings_summary(self, segment: str):
        """
        Fetch holdings summary.
        """

        payload = {"segment": segment}
        decrypted_data = self._post(self._HOLDINGS_SUMMARY_ROUTE, payload)

        return decrypted_data

    def _get(self, route, params=None):
        """Alias for sending a GET request."""
        return self._request(route, "GET", params=params)

    def _post(self, route, params=None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", params=params)

    def _put(self, route, params=None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", params=params)

    def _delete(self, route, params=None):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", params=params)

    def _request(self, url, method, params=None):
        """Make an HTTP request."""

        # Get public key
        public_key = self._get_public_key()

        # Encrypt public key
        api_encryption_key = encrypt_rsa(self.secret_key, public_key)

        # Set custom headers
        headers = self._get_headers(api_encryption_key)

        if self.debug:
            log.debug("Request: {method} {url} {params} {headers}".format(
                method=method, url=url, params=params, headers=headers))

        # prepare url query params
        if method in ["GET", "DELETE"]:
            query_params = params

        encrypted_payload = encrypt_aes(json.dumps(params), self.secret_key)

        try:
            req = self.session.request(method,
                                       url,
                                       json={'payload': encrypted_payload},
                                       params=query_params,
                                       headers=headers)
        # Any requests lib related exceptions are raised here - https://requests.readthedocs.io/en/latest/api/#exceptions
        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(
                code=req.status_code, content=req.content))

        # Validate the content type.
        if "json" in req.headers["content-type"]:
            try:
                data = req.json()
            except ValueError:
                raise exc.DataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=req.content))

            try:
                decrypted_data = decrypt_data(
                    data['data']['payload'], self.secret_key)
            except Exception:
                raise exc.DataException("Couldn't decrypt the response received from the server: {content}".format(
                    content=req.content))

            return decrypted_data
        elif "csv" in req.headers["content-type"]:
            return req.content
        else:
            raise exc.DataException("Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=req.headers["content-type"],
                content=req.content))
