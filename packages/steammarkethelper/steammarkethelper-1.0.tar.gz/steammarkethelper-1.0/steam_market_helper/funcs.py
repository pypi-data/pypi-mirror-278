import json
from time import sleep
from typing import List
from prettytable import PrettyTable
from .steam_market_helper_types import Item
from .api_call import make_api_call
from .parser import parse_market_history
from .settings import URL

__all__ = ["dump_item_list_to_json", "load_item_list_from_api", "load_item_list_from_json", "beautiful_table"]


def dump_item_list_to_json(path: str, item_list: List[Item]):
    with open(path, "w") as json_file:
        json.dump([*(item._asdict() for item in item_list)], json_file)


def load_item_list_from_api(is_test: bool, delay: int, is_log: bool) -> List[Item]:
    full_item_list = []
    total_items = make_api_call(URL.format("0")).total_items
    paginator = (start * 10 for start in range(0, (total_items // 10) + 1))
    for page_num, start in enumerate(paginator, start=1):
        market_api_response = make_api_call(URL.format(start))
        item_list = parse_market_history(market_api_response)
        full_item_list.extend(item_list)
        if is_log:
            beautiful_table(page_title=page_num, item_list=item_list)
        if is_test:
            break
        sleep(delay)
    return full_item_list


def load_item_list_from_json(path: str) -> List[Item]:
    with open(path, "r") as json_file:
        data: List[dict] = json.load(json_file)
        item_list = [Item(**item) for item in data]
        return item_list


def beautiful_table(page_title: int | str, item_list):
    title = f"Table #{page_title}" if isinstance(page_title, int) else page_title
    p_table = PrettyTable()
    p_table.title = title
    p_table.field_names = ["No", "transaction_type", "item_name", "item_type", "listed_on", "acted_on", "price",
                           "currency"]

    for i, item in enumerate(item_list, start=1):
        p_table.add_row([i, *item._asdict().values()])
    print(p_table, end="\n\n")
