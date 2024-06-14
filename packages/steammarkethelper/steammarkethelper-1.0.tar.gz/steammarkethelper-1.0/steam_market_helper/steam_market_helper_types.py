from collections import namedtuple
from enum import Enum

Item = namedtuple("Item", ["transaction_type", "item_name", "item_type", "listed_on", "acted_on", "price", "currency"])
MarketApiResponse = namedtuple("MarketApiResponse", ["html_page", "total_items"])


class TransactionType(Enum):
    sale = "sale"
    purchase = "purchase"
    listing = "listing"
    operation_canceled = "operation_canceled"
    all = "all"


class OrderType(Enum):
    desc = "desc"
    asc = "asc"


class FilterType(Enum):
    item_name = "item_name"
    item_type = "item_type"
    price = "price"
    no_filter = "no_filter"
