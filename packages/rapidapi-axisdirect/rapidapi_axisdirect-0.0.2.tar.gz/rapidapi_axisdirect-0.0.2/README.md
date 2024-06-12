# The Axis Direct Rapid API Python client


Python library for Axis Direct trading API based on the documentation provided by the Axis Direct (RAPID API by Axis Direct). 
[Axis Direct API](https://simplehai.axisdirect.in/RapidAPI).

RAPID API by Axis Direct is a powerful tool that expose many capabilities required to build a personalized Trading and Investment platform. Place orders, fetch user holdings, positions, orders, and more, with the simple HTTP API collection. This is not official library from the Axis Direct.


## Documentation

- [Official documentation](https://simplehai.axisdirect.in/RapidAPI)
- [Official REST API documentation](https://documenter.getpostman.com/view/33771924/2sA3BkasEf)

## Installing the client

You can install the latest release via pip

```
pip install --upgrade rapidapi-axisdirect
```

## Requirements

'client_id' and 'authorization_key' are required to use this client. Read the official documentation for more information [here](https://simplehai.axisdirect.in/RapidAPI)

## API usage

```python
from rapidapi_axisdirect import AxisAPIClient

axis_client = AxisAPIClient(client_id="your_api_key-xxx-xxx-x", authorization_key="your_authorization_keyxx-xxx-x")

# Initialize the initiate_sso method with $redirectURL to get the SSO login url.

login_url = axis_client.initiate_sso('https://app.example.com/redirect-here')

# Redirect the user to the login url obtained ('login_url')
# User will be redirected to the given $redirectURL with 'ssoId' after the SSO login flow.
# Once you have the ssoId, obtain the authToken and subAccountId

data = axis_client.authenticate_sso('ssoId')

axis_client.set_session(data['metadata']['accounts'][0]['subAccountId'], data['authToken']['token'])

# Place an order
try:
    order_resp = axis_client.place_order(order_ref_id="any_unique_remark",
                                script_id="11500112",
                                exchange='BSE',
                                transaction_type="BUY",
                                quantity=1,
                                segment='EQ,
                                order_type="MARKET",
                                product_type='DELIVERY',
                                validity_type='DAY')

    print("Order placed- response: ", order_resp)
except Exception as e:
    print("Failed. response: ", e.message)

# Fetch all orders by status
axis_client.get_order_book(order_status='open')

# Fetch the order history of a particular order.
axis_client.get_order_history("2024712987987")

# Get Security master
axis_client.get_security_master()

# Get the status of the market.
axis_client.get_market_status()

# Get holdings
axis_client.holdings(segment="EQ")
```


## Changelog

[Check release notes](https://github.com/abhaybraja/rapidapi-axisdirect/releases)