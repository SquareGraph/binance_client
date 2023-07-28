"""
Collection of enumerations related to Binance Constants
"""
from enum import Enum

__all__ = ["PositionSide", "Side", "OrderType", "TimeInForce"]


class PositionSide(Enum):
    """
    Enum for position side (after placing order)
    """
    LONG = "LONG"
    SHORT = "SHORT"
    BOTH = "BOTH"


class Side(Enum):
    """
    Enum for trade side (before placing order)
    """
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """
    Types of orders
    """
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"


class TimeInForce(Enum):
    """
    Forcing & execution methods
    """
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"
    GTE = "GTE"
    GTD = "GTD"
    DAY = "DAY"


class WorkingType(Enum):
    """
    WorkingType enumerations
    """
    MARKET = "MARK_PRICE"
    CONTRACT = "CONTRACT_PRICE"
