<h1 align="center">Futures, Spot and NFT - REST and Websocket API Python SDK for the Kraken Cryptocurrency Exchange 🐙</h1>

<div align="center">

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/btschwertfeger/python-kraken-sdk)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Generic badge](https://img.shields.io/badge/python-3.11+-blue.svg)](https://shields.io/)
[![Downloads](https://static.pepy.tech/personalized-badge/python-kraken-sdk?period=total&units=abbreviation&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/python-kraken-sdk)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typing](https://img.shields.io/badge/typing-mypy-informational)](https://mypy-lang.org/)
[![CI/CD](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml/badge.svg?branch=master)](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/btschwertfeger/python-kraken-sdk/branch/master/badge.svg)](https://app.codecov.io/gh/btschwertfeger/python-kraken-sdk)

[![OpenSSF ScoreCard](https://img.shields.io/ossf-scorecard/github.com/btschwertfeger/python-kraken-sdk?label=openssf%20scorecard&style=flat)](https://securityscorecards.dev/viewer/?uri=github.com/btschwertfeger/python-kraken-sdk)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8673/badge)](https://www.bestpractices.dev/projects/8673)

[![release](https://shields.io/github/release-date/btschwertfeger/python-kraken-sdk)](https://github.com/btschwertfeger/python-kraken-sdk/releases)
[![release](https://img.shields.io/pypi/v/python-kraken-sdk)](https://pypi.org/project/python-kraken-sdk/)
[![DOI](https://zenodo.org/badge/510751854.svg)](https://zenodo.org/badge/latestdoi/510751854)
[![Documentation Status Stable](https://readthedocs.org/projects/python-kraken-sdk/badge/?version=stable)](https://python-kraken-sdk.readthedocs.io/en/stable)

</div>

> ⚠️ This is an unofficial collection of REST and websocket clients for Spot and
> Futures trading on the Kraken cryptocurrency exchange using Python. Payward
> Ltd. and Kraken are in no way associated with the authors of this package and
> documentation.
>
> Please note that this project is independent and not endorsed by Kraken or
> Payward Ltd. Users should be aware that they are using third-party software,
> and the authors of this project are not responsible for any issues, losses, or
> risks associated with its usage.

## 📌 Disclaimer

There is no guarantee that this software will work flawlessly at this or later
times. Of course, no responsibility is taken for possible profits or losses.
This software probably has some errors in it, so use it at your own risk. Also
no one should be motivated or tempted to invest assets in speculative forms of
investment. By using this software you release the author(s) from any liability
regarding the use of this software.

---

## Features

General:

- command-line interface
- access both public and private, REST and websocket endpoints
- responsive error handling and custom exceptions
- extensive example scripts (see `/examples` and `/tests`)
- tested using the [pytest](https://docs.pytest.org/en/7.3.x/) framework
- releases are permanently archived at [Zenodo](https://zenodo.org/badge/latestdoi/510751854)
- releases before v2.0.0 also support Python 3.7+

Available Clients:

- NFT REST Clients
- Spot REST Clients
- Spot Websocket Clients (Websocket API v1 and v2)
- Spot Orderbook Clients (Websocket API v1 and v2)
- Futures REST Clients
- Futures Websocket Client

Documentation:

- [https://python-kraken-sdk.readthedocs.io/en/stable](https://python-kraken-sdk.readthedocs.io/en/stable)
- [https://python-kraken-sdk.readthedocs.io/en/latest](https://python-kraken-sdk.readthedocs.io/en/latest)

---

## ❗️ Attention

**ONLY** tagged releases are available at PyPI. So the content of the master may
not match with the content of the latest release. - Please have a look at the
release specific READMEs and changelogs.

It is also recommended to _pin the used version_ to avoid unexpected behavior on
new releases.

---

## Table of Contents

- [ Installation and setup ](#installation)
- [ Command-line interface ](#cliusage)
- [ SDK Usage Hints ](#sdkusage)
- [ Spot Clients ](#spotusage)
  - [REST API](#spotrest)
  - [Websocket API V2](#spotws)
- [ Futures Clients ](#futuresusage)
  - [REST API](#futuresrest)
  - [Websocket API](#futuresws)
- [ NFT Clients ](#nftusage)
- [ Troubleshooting ](#trouble)
- [ Contributions ](#contribution)
- [ Notes ](#notes)
- [ References ](#references)

<a name="installation"></a>

# 🛠 Installation and setup

### 1. Install the package into the desired environment

```bash
python3 -m pip install python-kraken-sdk
```

### 2. Register at [Kraken](https://www.kraken.com) and generate API keys

- Spot Trading: https://www.kraken.com/u/security/api
- Futures Trading: https://futures.kraken.com/trade/settings/api (see _[help](https://docs.futures.kraken.com/#introduction-generate-api-keys)_)
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

### 3. Start using the provided example scripts

### 4. Error handling

If any unexpected behavior occurs, please check <b style="color: yellow">your
API permissions</b>, <b style="color: yellow">rate limits</b>, update the
python-kraken-sdk, see the [Troubleshooting](#trouble) section, and if the error
persists please open an issue.

<a name="cliusage"></a>

# 📍 Command-line interface

The python-kraken-sdk provides a command-line interface to access the Kraken API
using basic instructions while performing authentication tasks in the
background. The Spot, NFT and Futures API are accessible and follow the pattern
`kraken {spot,futures} [OPTIONS] URL`. See examples below.

```bash
# get server time
kraken spot https://api.kraken.com/0/public/Time
{'unixtime': 1716707589, 'rfc1123': 'Sun, 26 May 24 07:13:09 +0000'}

# get user's balances
kraken spot --api-key=<api-key> --secret-key=<secret-key> -X POST https://api.kraken.com/0/private/Balance
{'ATOM': '17.28229999', 'BCH': '0.0000077100', 'ZUSD': '1000.0000'}

# get user's trade balances
kraken spot --api-key=<api-key> --secret-key=<secret-key> -X POST https://api.kraken.com/0/private/TradeBalance --data '{"asset": "DOT"}'
{'eb': '2.8987347115', 'tb': '1.1694303513', 'm': '0.0000000000', 'uv': '0', 'n': '0.0000000000', 'c': '0.0000000000', 'v': '0.0000000000', 'e': '1.1694303513', 'mf': '1.1694303513'}

# get 1D candles for a futures instrument
kraken futures https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d
{'candles': [{'time': 1625616000000, 'open': '34557.84000000000', 'high': '34803.20000000000', 'low': '33816.32000000000', 'close': '33880.22000000000', 'volume': '0' ...

# get user's open futures positions
kraken futures --api-key=<api-key> --secret-key=<secret-key> https://futures.kraken.com/derivatives/api/v3/openpositions
{'result': 'success', 'openPositions': [], 'serverTime': '2024-05-26T07:15:38.91Z'}
```

... All endpoints of the Kraken Spot and Futurs API can be accessed like that.

<a name="sdkusage"></a>

# 📍 SDK Usage Hints

The python-kraken-sdk provides lots of functions to easily access most of the
REST and websocket endpoints of the Kraken Cryptocurrency Exchange API. Since
these endpoints and their parameters may change, all implemented endpoints are
tested on a regular basis.

If certain parameters or settings are not available, or
specific endpoints are hidden and not implemented, it is always possible to
execute requests to the endpoints directly using the `_request` method provided
by any client. This is demonstrated below.

```python
from kraken.spot import User

user = User(key="<your-api-key>", secret="<your-secret-key>")
print(user._request(method="POST", uri="/0/private/Balance"))
```

<a name="spotusage"></a>

# 📍 Spot Clients

A template for Spot trading using both websocket and REST clients can be found
in `examples/spot_trading_bot_template_v2.py`.

For those who need a realtime order book - a script that demonstrates how to
maintain a valid order book using the Orderbook client can be found in
`examples/spot_orderbook_v2.py`.

<a name="spotrest"></a>

## Spot REST API

The Kraken Spot REST API offers many endpoints for almost every use-case. The
python-kraken-sdk aims to provide all of them - split in User, Market, Trade,
Funding and Staking (Earn) related clients.

The following code block demonstrates how to use some of them. More examples
can be found in `examples/spot_examples.py`.

```python
from kraken.spot import Earn, User, Market, Trade, Funding

def main():
    key = "kraken-public-key"
    secret = "kraken-secret-key"

    # ____USER________________________
    user = User(key=key, secret=secret)
    print(user.get_account_balance())
    print(user.get_open_orders())
    # …

    # ____MARKET____
    market = Market()
    print(market.get_ticker(pair="BTCUSD"))
    # …

    # ____TRADE_________________________
    trade = Trade(key=key, secret=secret)
    print(trade.create_order(
         ordertype="limit",
         side="buy",
         volume=1,
         pair="BTC/EUR",
         price=20000
    ))
    # …

    # ____FUNDING___________________________
    funding = Funding(key=key, secret=secret)
    print(
        funding.withdraw_funds(
            asset="DOT", key="MyPolkadotWallet", amount=200
        )
    )
    print(funding.cancel_withdraw(asset="DOT", refid="<some id>"))
    # …

    # ____EARN________________________
    earn = Earn(key=key, secret=secret)
    print(earn.list_earn_strategies(asset="DOT"))
    # …

if __name__ == "__main__":
    main()
```

<a name="spotws"></a>

## Spot Websocket API V2

Kraken offers two versions of their websocket API (V1 and V2). Since V2 is
offers more possibilities, is way faster and easier to use, only those examples
are shown below. For using the websocket API V1 please have a look into the
`examples/spot_ws_examples_v1.py`.

The documentation for both API versions can be found here:

- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2

Note that authenticated Spot websocket clients can also un-/subscribe from/to
public feeds.

The example below can be found in an extended way in
`examples/spot_ws_examples_v2.py`.

```python
import asyncio
from kraken.spot import KrakenSpotWSClientV2

async def main():
    key = "spot-api-key"
    secret = "spot-secret-key"

    class Client(KrakenSpotWSClientV2):
        """Can be used to create a custom trading strategy"""

        async def on_message(self, message):
            """Receives the websocket messages"""
            if message.get("method") == "pong" \
                or message.get("channel") == "heartbeat":
                return

            print(message)
            # here we can access lots of methods, for example to create an order:
            # if self.is_auth:  # only if the client is authenticated …
            #     await self.send_message(
            #         message={
            #             "method": "add_order",
            #             "params": {
            #                 "limit_price": 1234.56,
            #                 "order_type": "limit",
            #                 "order_userref": 123456789,
            #                 "order_qty": 1.0,
            #                 "side": "buy",
            #                 "symbol": "BTC/USD",
            #                 "validate": True,
            #             },
            #         }
            #     )
            # … it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient.
            # You can also un-/subscribe here using self.subscribe/self.unsubscribe.

    # Public/unauthenticated websocket client
    client = Client()  # only use this one if you don't need private feeds

    await client.subscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    await client.subscribe(
        params={"channel": "book", "depth": 25, "symbol": ["BTC/USD"]}
    )
    # wait because unsubscribing is faster than unsubscribing … (just for that example)
    await asyncio.sleep(3)
    # print(client.active_public_subscriptions) # to list active subscriptions
    await client.unsubscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    # …

    # Per default, the authenticated client starts two websocket connections,
    # one for authenticated and one for public messages. If there is no need
    # for a public connection, it can be disabled using the ``no_public``
    # parameter.
    client_auth = Client(key=key, secret=secret, no_public=True)
    await client_auth.subscribe(params={"channel": "executions"})

    while not client.exception_occur and not client_auth.exception_occur:
        await asyncio.sleep(6)
    return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        # The websocket client will send {'event': 'asyncio.CancelledError'}
        # via on_message so you can handle the behavior/next actions
        # individually within your strategy.
```

---

<a name="futuresusage"></a>

# 📍 Futures Clients

Kraken provides a sandbox environment at https://demo-futures.kraken.com for
Futures paper trading. When using these API keys you have to set the `sandbox`
parameter to `True` when instantiating the respective client.

A template for Futures trading using both websocket and REST clients can be
found in `examples/futures_trading_bot_template.py`.

The Kraken Futures API documentation can be found here:

- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

<a name="futuresrest"></a>

## Futures REST API

As the Spot API, Kraken also offers a REST API for Futures. Examples on how to
use the python-kraken-sdk for Futures are shown in
`examples/futures_examples.py` and listed in a shorter ways below.

```python
from kraken.futures import Market, User, Trade, Funding

def main():

    key = "futures-api-key"
    secret = "futures-secret-key"

    # ____USER________________________
    user = User(key=key, secret=secret) # optional: sandbox=True
    print(user.get_wallets())
    print(user.get_open_orders())
    print(user.get_open_positions())
    print(user.get_subaccounts())
    # …

    # ____MARKET____
    market = Market()
    print(market.get_ohlc(tick_type="trade", symbol="PI_XBTUSD", resolution="5m"))

    priv_market = Market(key=key, secret=secret)
    print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_execution_events())
    # …

    # ____TRADE_________________________
    trade = Trade(key=key, secret=secret)
    print(trade.get_fills())
    print(trade.create_batch_order(
        batchorder_list = [{
            "order": "send",
            "order_tag": "1",
            "orderType": "lmt",
            "symbol": "PI_XBTUSD",
            "side": "buy",
            "size": 1,
            "limitPrice": 12000,
            "cliOrdId": "some-client-id"
        }, {
            "order": "send",
            "order_tag": "2",
            "orderType": "stp",
            "symbol": "PI_XBTUSD",
            "side": "buy",
            "size": 1,
            "limitPrice": 10000,
            "stopPrice": 11000,
        }, {
            "order": "cancel",
            "order_id": "e35dsdfsdfsddd-8a30-4d5f-a574-b5593esdf0",
        }, {
            "order": "cancel",
            "cliOrdId": "another-client-id",
        }],
    ))
    print(trade.cancel_all_orders())
    print(
        trade.create_order(
            orderType="lmt",
            side="buy",
            size=1,
            limitPrice=4,
            symbol="pf_bchusd"
        )
    )
    # …

    # ____FUNDING___________________________
    funding = Funding(key=key, secret=secret)
    # …

if __name__ == "__main__":
    main()
```

<a name="futuresws"></a>

## Futures Websocket API

Not only REST, also the websocket API for Kraken Futures is available. Examples
are shown below and demonstrated in `examples/futures_ws_examples.py`.

- https://docs.futures.kraken.com/#websocket-api

Note: Authenticated Futures websocket clients can also un-/subscribe from/to
public feeds.

```python
import asyncio
from kraken.futures import KrakenFuturesWSClient

async def main():

    key = "futures-api-key"
    secret = "futures-secret-key"

    class Client(KrakenFuturesWSClient):

        async def on_message(self, event):
            print(event)

    # Public/unauthenticated websocket connection
    client = Client()

    products = ["PI_XBTUSD", "PF_ETHUSD"]

    # subscribe to a public websocket feed
    await client.subscribe(feed="ticker", products=products)
    # await client.subscribe(feed="book", products=products)
    # …

    # unsubscribe from a public websocket feed
    # await client.unsubscribe(feed="ticker", products=products)

    # Private/authenticated websocket connection (+public)
    client_auth = Client(key=key, secret=secret)
    # print(client_auth.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await client_auth.subscribe(feed="fills")
    await client_auth.subscribe(feed="open_positions")
    await client_auth.subscribe(feed="open_orders")
    # …

    # unsubscribe from a private/authenticated websocket feed
    await client_auth.unsubscribe(feed="fills")

    while True:
        await asyncio.sleep(6)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # do some exception handling …
        pass
```

---

<a name="nftusage"></a>

# 📍 NFT REST Clients

The Kraken NFT REST API offers endpoints for accessing the market and trade API
provided by Kraken. To access the private (trade) endpoints, you have to provide
API keys - same as for the Spot REST API.

The following code excerpt demonstrates the usage. Please have a look into
`tests/nft/*.py` for more examples.

```python
from kraken.nft import  Market, Trade

def main():
    key = "kraken-public-key"
    secret = "kraken-secret-key"

    market = Market()
    print(market.get_nft(nft_id="NT4GUCU-SIJE2-YSQQG2", currency="USD"))

    trade = Trade(key=key, secret=secret)
    print(trade.create_auction(
        auction_currency="ETH",
        nft_id=["NT4EFBO-OWGI5-QLO7AG"],
        auction_type="fixed",
        auction_params={
            "allow_offers": True,
            "ask_price": 100000,
        },
    ))

if __name__ == "__main__":
    main()
```

---

<a name="contribution"></a>

# 🆕 Contributions

… are welcome - but:

- First check if there is an existing issue or PR that addresses your
  problem/solution. If not - create one first - before creating a PR.
- Typo fixes, project configuration, CI, documentation or style/formatting PRs
  will be rejected. Please create an issue for that.
- PRs must provide a reasonable, easy to understand and maintain solution for an
  existing problem. You may want to propose a solution when creating the issue
  to discuss the approach before creating a PR.
- Please have a look at [CONTRIBUTION.md](./CONTRIBUTING.md).

---

<a name="trouble"></a>

# 🚨 Troubleshooting

- Check if you downloaded and installed the **latest version** of the
  python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the
  respective endpoints.
- If you get some Cloudflare or **rate limit errors**, please check your Kraken
  Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce
  calculation is based on timestamps and a sent nonce must always be the highest
  nonce ever sent of that API key. Having multiple algorithms using the same
  keys will result in invalid nonce errors.

---

<a name="notes"></a>

# 📝 Notes

The versioning scheme follows the pattern `v<Major>.<Minor>.<Patch>`. Here's what each part signifies:

- **Major**: This denotes significant changes that may introduce new features or
  modify existing ones. It's possible for these changes to be breaking, meaning
  backward compatibility is not guaranteed. To avoid unexpected behavior, it's
  advisable to specify at least the major version when pinning dependencies.
- **Minor**: This level indicates additions of new features or extensions to
  existing ones. Typically, these changes do not break existing implementations.
- **Patch**: Here, you'll find bug fixes, documentation updates, and changes
  related to continuous integration (CI). These updates are intended to enhance
  stability and reliability without altering existing functionality.

Coding standards are not always followed to make arguments and function names as
similar as possible to those of the Kraken API documentations.

<a name="references"></a>

# 🔭 References

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
