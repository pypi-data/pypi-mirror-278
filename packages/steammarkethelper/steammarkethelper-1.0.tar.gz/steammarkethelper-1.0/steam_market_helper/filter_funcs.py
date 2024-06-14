from typing import List
from .steam_market_helper_types import Item, TransactionType, FilterType, OrderType


def get_sorted_item_list(item_list: List[Item], transaction: str, filter: str, order: str) -> List[Item]:
    transaction_type = TransactionType[transaction]
    filter = FilterType[filter]
    order = OrderType[order]

    item_list_by_transaction_type = get_item_list_by_transaction_type(item_list, transaction_type)
    filtered_item_list = get_filtered_item_list(item_list_by_transaction_type, filter, order)
    return filtered_item_list


def get_item_list_by_transaction_type(item_list: List[Item], transaction_type: TransactionType) -> List[Item]:
    tt = transaction_type.value
    if tt == "all":
        return item_list
    return list(filter(lambda item: item.transaction_type == tt, item_list))


def get_filtered_item_list(item_list: List[Item], filter: FilterType, order: OrderType) -> List[Item]:
    filter = filter.value
    is_reverse = True if order.value == "desc" else False
    if filter == "no_filter":
        return item_list
    return sorted(item_list, key=lambda item: getattr(item, filter), reverse=is_reverse)
