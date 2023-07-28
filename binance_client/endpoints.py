"""
Collection of endpoint-related classes
"""
import os
from enum import Enum
from dataclasses import dataclass, fields
from pathlib import Path

from .enums import Side, PositionSide


__all__ = [
    "DEFAULT_RCV_WIND",
    "BinanceMarkets",
    "Connection",
    "ExchangeKeys",
    "API",
    "TestConnectivity",
    "ServerTime",
    "ExchangeInfo",
    "ExchangeInfo",
    "RecentTrades",
    "MarkPrice",
    "OpenOrders",
    "OpenOrder",
    "FuturesBalance",
    "AccountInformation",
    "PositionInformation",
    "AllOrders",
    "UserTrades",
    "CurrentPositionMode",
    "ChangePositionMode",
    "NewOrder",
    "CancelOrder",
    "CancelAllOpenOrders",
    "PositionInformation",
]

DEFAULT_RCV_WIND = 5000


class BinanceMarkets(Enum):
    """
    Abstraction for selecting type of exchange
    """

    TESTNET_FUTURES: str = "https://testnet.binancefuture.com"
    FUTURES: str = "https://fapi.binance.com"
    SPOT: str = "https://api.binance.com"


class Connection(Enum):
    """
    Abstraction for picking market type (spot/futures/futures-coin)
    """

    API: str = "/api"
    FAPI: str = "/fapi"
    DAPI: str = "/dapi"


@dataclass
class ExchangeKeys:
    """
    Container for keeping order of Exchange Keys
    """

    SECRET: str
    API: str
    EXCHANGE: BinanceMarkets

    def __post_init__(self):
        self.EXCHANGE = self.EXCHANGE.name.upper()

    @classmethod
    def from_env(
        cls,
        envpath: Path = "../.env",
        exchange: BinanceMarkets = BinanceMarkets.SPOT,
        exchange_env_prefix: str = "BINANCE",
    ):
        """
        Creates an instance of class from .env file
        Example env names: BINANCE_FUTURES_API_KEY, BINANCE_SPOT_SECRET_KEY

        Env var name have to be constructed as: PREFIX_BinanceMarkets.__member___API_KEY/SECRET_KEY

        Parameters:
            envpath: Path, to .env file
            exchange: BinanceMarkets.__member__
            exchange_env_prefix: default BINANCE.

        Returns:
            ExchangeKeys instance
        """

        # exchange = exchange.name.upper()

        with open(envpath) as f:
            for line in f:
                key, value = line.strip().split("=")
                os.environ[key] = value

        apikey = f"{exchange_env_prefix}_{exchange.name}_API_KEY"
        secretkey = f"{exchange_env_prefix}_{exchange.name}_SECRET_KEY"

        return cls(os.getenv(secretkey), os.getenv(apikey), exchange)


@dataclass
class API:
    """
    Parent class for subclassing instances that handles Binance methods.
    """

    EXCLUDE = ["METHOD", "ENDPOINT", "SIGNATURE"]

    def query_string(self) -> str:
        """
        Creates a REST api query string

        Returns:
            str
        """
        payload = {}
        for item in fields(self):
            if item.name not in API.EXCLUDE:
                attr = getattr(self, item.name)
                if attr is not None:
                    payload.update({item.name: attr})

        return "&".join([f"{key}={val}" for key, val in payload.items()])


# GENERAL
@dataclass
class TestConnectivity(API):
    """
    Binance TestConnectivity method
    """

    METHOD: str = "GET"
    ENDPOINT: str = "/v1/ping"
    SIGNATURE: bool = False


@dataclass
class ServerTime(API):
    """
    Binance ServerTime method
    """

    METHOD: str = "GET"
    ENDPOINT: str = "/v1/time"
    SIGNATURE: bool = False


@dataclass
class ExchangeInfo(API):
    """
    Binance ExchangeInfo method
    """

    METHOD: str = "GET"
    ENDPOINT: str = "/v1/exchangeInfo"
    SIGNATURE: bool = False


@dataclass
class RecentTrades(API):
    """
    Binance RecentTrades method
    """

    symbol: str
    limit: int = 1000
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/trades"
    SIGNATURE: bool = False


@dataclass
class MarkPrice(API):
    """
    Binance MarketPrice method
    """

    symbol: str
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/premiumIndex"
    SIGNATURE: bool = False


# ACCOUNT
@dataclass
class OpenOrders(API):
    """
    Binance OpenOrder method
    """

    timestamp: str
    symbol: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/openOrders"
    SIGNATURE: bool = True


@dataclass
class OpenOrder(API):
    """
    Binance OpenOrders method
    """

    timestamp: str
    symbol: str
    orderId: int
    origClientOrderId: str = None
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/openOrder"
    SIGNATURE: bool = True


@dataclass
class FuturesBalance(API):
    """
    Binance FuturesBalance method
    """

    timestamp: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v2/balance"
    SIGNATURE: bool = True


@dataclass
class AccountInformation(API):
    """
    Binance AccountInformation method
    """

    timestamp: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v2/account"
    SIGNATURE: bool = True


@dataclass
class PositionInformation(API):
    """
    Binance PositionInformation method
    """

    timestamp: str
    symbol: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v2/positionRisk"
    SIGNATURE: bool = True


@dataclass
class AllOrders(API):
    """
    Binance AllOrders method
    """

    timestamp: str
    symbol: str
    orderId: int = None
    startTime: int = None
    endTime: int = None
    limit: int = 500
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/allOrders"
    SIGNATURE: bool = True


@dataclass
class UserTrades(API):
    """
    Binance UserTrades method
    """

    timestamp: str
    symbol: str
    orderId: int = None
    startTime: int = None
    endTime: int = None
    limit: int = 500
    fromId: int = None
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = f"/v1/userTrades"
    SIGNATURE: bool = True


# Account & Trades
@dataclass
class CurrentPositionMode(API):
    """
    Binance CurrentPositionMode method
    """

    timestamp: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "GET"
    ENDPOINT: str = "/v1/positionSide/dual"
    SIGNATURE: bool = True


@dataclass
class ChangePositionMode(API):
    """
    Binance ChangePositionMode method
    """

    timestamp: str
    dualSidePosition: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "POST"
    ENDPOINT: str = "/v1/positionSide/dual"
    SIGNATURE: bool = True


@dataclass
class NewOrder(API):
    """
    Binance NewOrder method
    """

    timestamp: str
    symbol: str
    side: Side
    positionSide: PositionSide
    type: Enum
    quantity: float = None
    price: float = None
    timeInForce: Enum = None
    stopPrice: float = None
    activationPrice: float = None
    callbackRate: Enum = None
    closePosition: str = "false"
    reduceOnly: str = None
    newClientOrderId: str = None
    workingType: Enum = None
    priceProtect: str = None
    newOrderRespType: Enum = "ACK"
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "POST"
    ENDPOINT: str = f"/v1/order"
    SIGNATURE: bool = True

    def __post_init__(self):
        self.side = self.side.value  # overwrite class enum with correspodning value
        self.positionSide = self.positionSide.value
        self.type = self.type.value
        self.timeInForce = (
            self.timeInForce.value if self.timeInForce is not None else None
        )
        self.workingType = (
            self.workingType.value if self.workingType is not None else None
        )


@dataclass
class CancelOrder(API):
    """
    Binance CancelOrder method
    """

    timestamp: str
    symbol: str
    orderId: str
    origClientOrderId: str = None
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "DELETE"
    ENDPOINT: str = "/v1/order"
    SIGNATURE: bool = True


@dataclass
class CancelAllOpenOrders(API):
    """
    Binance CancelAllOpenOrders method
    """

    timestamp: str
    symbol: str
    recvWindow: int = DEFAULT_RCV_WIND
    METHOD: str = "DELETE"
    ENDPOINT: str = "/v1/allOpenOrders"
    SIGNATURE: bool = True