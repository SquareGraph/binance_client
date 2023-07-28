"""
Client module consists of only Client class that handles get_timestamp & call methods
"""
import hashlib
import hmac
import time
from typing import Dict, Literal, get_type_hints

import requests
from .endpoints import BinanceMarkets, Connection, ExchangeKeys, ServerTime, API

__all__ = ["Client"]


class Client:
    """
    Main abstraction of binance_client library. Instance is used to make API calls.

    Parameters:
        exchange: one of BinanceMarkets.__members__
        api_type: one of Connection.__members__
        exchange_keys: ExchangeKeys instance

    Methods:
        Client.get_timestamp()
        Client.call()
    """

    def __new__(
        cls, exchange: BinanceMarkets, api_type: Connection, exchange_keys: ExchangeKeys
    ) -> object:

        assert exchange_keys.EXCHANGE == exchange.name, AssertionError(
            "Defined keys doesn't match defined market"
        )

        for key, value in get_type_hints(cls.__new__).items():
            if not isinstance(key, value):
                raise TypeError(f"{key} have to be an instance of {value}.")

        return object.__new__(cls)

    def __init__(
        self,
        exchange: BinanceMarkets,
        api_type: Connection,
        exchange_keys: ExchangeKeys,
    ) -> None:
        """
        On initialization creates following attributes:
        self.exchange, self.api_type, self.url, self.API_KEY, self.SECRET_KEY

        Parameters:
            exchange: one of BinanceMarkets.__members__
            api_type: one of Connection.__members__
            exchange_keys: ExchangeKeys instance
        """

        self.exchange = exchange
        self.api_type = api_type
        self.url = self.exchange.value + self.api_type.value
        self.API_KEY = exchange_keys.API
        self.SECRET_KEY = exchange_keys.SECRET

    def __get_headers(self) -> Dict:
        return {"X-MBX-APIKEY": self.API_KEY}


    def get_timestamp(self, type_: Literal["Local", "Server"] = "Local") -> str:
        """
        Returns timestamp value for making api calls.
        Part of the binance methods require passing the timestamp,
        and depending on circumstances, one may choose to pick server-based or local timestamp.
        This method returns it.

        Parameters:
            type: Literal['Local','Server'], default 'Local'

        Returns:
            str(timestamp)
        """
        type_ = type_.lower()
        if type_ == "local":
            return str(int(time.time() * 1000))
        if type_ == "exchange":
            return str(int(float(self.call(ServerTime())["serverTime"])))

        raise TypeError("Wrong type, have to be one of Local or Exchange")

    def call(self, api: API) -> str:
        """
        Makes a call to the given method in Binance API.
        A method is a subclass of API class from endpoints submodule.

        Parameters:
            api: a method, subclass of API

        Returns:
             Str, if answer is of type 2XX, than it's a string of json.
        """

        query_string = api.query_string()
        url = self.url + api.ENDPOINT + "?" + query_string

        if api.SIGNATURE:
            signature = hmac.new(
                self.SECRET_KEY.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()

            url += f"&signature={signature}"

        response = requests.request(
            method=api.METHOD, url=url, headers=self.__get_headers()
        )

        if response.status_code > 199 & response.status_code < 300:
            return response.json()

        print(response.status_code)
        return response
