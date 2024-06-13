# circle-developer-controlled-wallets
Developer-Controlled Wallets API documentation.

- API version: 1.0
- Package version: 1.1.0

## Requirements.

Python 3.7+

## Installation
### pip install

```sh
pip install circle-developer-controlled-wallets
```

Then import the package:
```python
from circle.web3 import developer_controlled_wallets
```


## Usage

1. Generate an API key, if you haven't already, in the [Web3 Services Console](https://console.circle.com/). This API key will be used for authentication and authorization when making requests to Circle's APIs. API key can be set by environment variable or function parameter.

```sh
export CIRCLE_WEB3_API_KEY="Your API KEY"
```

2. Register an entity secret following Circle's [Developer-Controlled QuickStart](https://learn.circle.com/quickstarts/dev-controlled-wallets). This step ensures that your account is correctly set up to interact with Circle's APIs. Entity secret can be set by environment variable or function parameter

```sh
export CIRCLE_ENTITY_SECRET="Your entity secret"
```

3. Initiate API client

```python
from circle.web3 import utils

client = utils.init_developer_controlled_wallets_client(api_key="Your API KEY", entity_secret="Your entity secret")
```

4. Interact with the client:

```python
from circle.web3 import developer_controlled_wallets

api_instance = developer_controlled_wallets.WalletSetsApi(client)

# create wallet sets
try:
    request = developer_controlled_wallets.CreateDeveloperWalletSetRequest.from_dict({
        "name": "my_wallet_set"
    })
    api_instance.create_wallet_set(request)
except developer_controlled_wallets.ApiException as e:
    print("Exception when calling WalletSetsApi->create_wallet_set: %s\n" % e)

# list wallet sets
try:
    response = api_instance.list_wallet_sets()
    for wallet_set in response.data.wallet_sets:
        print(wallet_set.id)
except developer_controlled_wallets.ApiException as e:
    print("Exception when calling WalletSetsApi->list_wallet_sets: %s\n" % e)
```

We recommend reading through the official [documentation](https://developers.circle.com/w3s) and [QuickStart guides](https://learn.circle.com/) mentioned above to ensure a smooth setup and usage experience.


## Configuration

The client accept following configuration parameters:

Option | Required | Description
------------ | ------------- | -------------
api_key | Yes | Api Key that is used to authenticate against Circle APIs. Must be provided by ether env variable or function parameter
entity_secret | Yes | Your configured entity secret. Must be provided by ether env variable or function parameter.
host | No | Optional base URL to override the default: https://api.circle.com/v1/w3s.
user_agent | No | Optional custom user agent request header. We will prepend it to default user agent header if provided.


## Need help or have questions?

Here are some helpful links, if you encounter any issues or have questions about this SDK:

- 📖 [Getting started](https://learn.circle.com/quickstarts/developer-controlled-wallets): Check out our official Developer-Controlled Wallets QuickStart.
- 🎮 [Join our Discord Community](https://discord.com/invite/buildoncircle): Engage, learn, and collaborate.
- 🛎 [Visit our Help-Desk Page](https://support.usdc.circle.com/hc/en-us/p/contactus?_gl=1*1va6vat*_ga*MTAyNTA0NTQ2NC4xNjk5NTYyMjgx*_ga_GJDVPCQNRV*MTcwMDQ5Mzg3Ny4xNC4xLjE3MDA0OTM4ODQuNTMuMC4w): Dive into curated FAQs and guides.
- 📧 [Direct Email](mailto:customer-support@circle.com): We're always a message away.
- 📖 [Read docs](https://developers.circle.com/w3s/docs?_gl=1*15ozb5b*_ga*MTAyNTA0NTQ2NC4xNjk5NTYyMjgx*_ga_GJDVPCQNRV*MTcwMDQ5Mzg3Ny4xNC4xLjE3MDA0OTM4ODQuNTMuMC4w): Check out our developer documentation.
Happy coding!
