from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="UTF8")
    cookie: str


settings = Settings()

URL = "https://steamcommunity.com/market/myhistory/render/?query=&start={}&count=10"
HEADERS = {
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Cookie": settings.cookie,
    "Host": "steamcommunity.com",
    "Referer": "https://steamcommunity.com/market/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "X-Prototype-Version": "1.7",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": """Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24""",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS"
}
