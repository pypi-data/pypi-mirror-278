from requests import get
from .steam_market_helper_types import MarketApiResponse
from .settings import HEADERS


def make_api_call(url: str) -> MarketApiResponse:
    response = get(url, headers=HEADERS).json()
    return MarketApiResponse(html_page=response["results_html"], total_items=response["total_count"])
