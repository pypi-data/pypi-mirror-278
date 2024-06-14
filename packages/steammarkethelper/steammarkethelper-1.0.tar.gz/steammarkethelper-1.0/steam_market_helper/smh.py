from time import sleep
import click

from steam_market_helper.steam_market_helper_types import TransactionType, OrderType, FilterType
from steam_market_helper.funcs import *
from steam_market_helper.filter_funcs import get_sorted_item_list


@click.command()
@click.argument("path")
@click.option("-d", "--delay", default=0, help="Set delay between api calls")
@click.option("--test", is_flag=True, help="Enable test mode (dump one page)")
@click.option("--no-log", is_flag=True, help="Disable log")
def init(no_log, test, path=".", delay=0):
    path = "./smh.json" if path == "." else path
    click.echo("Initializing Steam Market...")
    sleep(2)
    item_list = load_item_list_from_api(is_test=test, delay=delay, is_log=not no_log)
    dump_item_list_to_json(path=path, item_list=item_list)

    click.echo("Steam Market successfully initialized!")
    click.echo(f"Your data stores in: {path}")


@click.command()
@click.option("-p", "--path", default="./smh.json", help="Path to item data in json file")
@click.option("-d", "--delay", default=0, help="Set delay between api calls")
@click.option("--no-cached", is_flag=True, help="Do not use local files")
@click.option("--test", is_flag=True, help="Enable test mode (get one page)")
@click.option("-tt", "--transaction-type", type=click.Choice([field.value for field in TransactionType]), default="all")
@click.option("-f", "--filter", type=click.Choice([field.value for field in FilterType]), default="no_filter")
@click.option("-o", "--order", type=click.Choice([field.value for field in OrderType]), default="desc")
@click.option("-t", "--title", default="Item List Table", help="Set custom title for table")
@click.option("--stats", is_flag=True, help="Get addition statistics")
def getlist(test: bool, stats: bool, no_cached: bool, path="./smh.json", delay: int = 0,
            transaction_type: str = "all",
            filter: str = "no_filter",
            order: str = "desc",
            title: str = "Item List Table"):
    path = "./smh.json" if path == "." else path

    if no_cached:
        click.echo(click.echo("Initializing Steam Market..."))
        sleep(2)
        item_list = load_item_list_from_api(is_test=test, delay=delay, is_log=False)
    else:
        item_list = load_item_list_from_json(path=path)
    sorted_list = get_sorted_item_list(item_list=item_list, transaction=transaction_type, filter=filter, order=order)
    beautiful_table(page_title=title, item_list=sorted_list)

    if stats:
        currency = sorted_list[0].currency
        total = sum([item.price for item in sorted_list])

        click.echo(f"1.Number of items: {len(sorted_list)}")
        click.echo(f"2.Total: {total} {currency}")


@click.group()
def smh_commands():
    pass


smh_commands.add_command(init)
smh_commands.add_command(getlist)

if __name__ == "__main__":
    smh_commands()
