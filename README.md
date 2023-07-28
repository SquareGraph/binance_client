# binance_client
Python's lightweight client for Binance. Probably in the future will become integral module of bigger package I'm working on.

# Main abstraction & Usage example

Getting response from API is very simple. First we have to initialize binance_client.Client.
Methods works as dataclasses, so after we create an instance of Client, we can pass a method as an argument to the Client.call() method.

```
import binance_client as bc

market = bc.BinanceMarkets.FUTURES
client = bc.Client(market, bc.Connection.FAPI, bc.ExchangeKeys(SECRET='XXX', API='XXX', market)
method = bc.PositionInformation(client.get_timestamp(), 'BTCUSDT')
response = client.call(method)

print(response)
```

Above snippet will return output from the PositionInformation method of Binance API, for USDT-Futures.
