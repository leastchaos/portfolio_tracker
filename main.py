"""
load exchange client
fetch balance to dataframe
set sheet with dataframe
"""
import asyncio
from typing import Any

import ccxt.async_support as ccxt
import pandas as pd
import yaml

from client import get_ccxt_clients_from_yml
from google_helper import get_workbook, set_sheet_with_df

USD_LIST = ["USDT", "USDC", "USD", "TUSD"]
CONFIG_FILE_LOCATION = "./config.yml"


def get_price(tickers: dict[str, Any], asset: str) -> float:
    """get price"""
    for usd in USD_LIST:
        ticker = tickers.get(asset + "/" + usd)
        if ticker is not None:
            break
    else:
        print("no ticker for", asset)
        return 0
    return ticker.get("last") or ticker.get("close") or ticker.get("bid") or 0


async def fetch_total_usd(client: ccxt.Exchange) -> float:
    """
    fetch balance to dataframe
    """
    total_usd = 0
    balance = await client.fetch_balance()
    tickers = await client.fetch_tickers()
    total: dict[str, float] = balance["total"]
    for asset, amount in total.items():
        if amount == 0.0:
            continue
        if asset in USD_LIST:
            total_usd += amount
            continue
        price = get_price(tickers, asset)
        total_usd += amount * price
    return total_usd


def load_config(file_location: str = CONFIG_FILE_LOCATION) -> dict[str, str]:
    """load config"""
    with open(file_location, "r") as f:
        yml_data: dict = yaml.safe_load(f)
    return yml_data


async def main():
    """main"""
    config = load_config()
    clients = get_ccxt_clients_from_yml()
    workbook = get_workbook(config["workbook_name"])
    try:
        while True:
            balances = await asyncio.gather(
                *[fetch_total_usd(client) for client in clients.values()]
            )
            client_balances = {
                account_name: [balance]
                for account_name, balance in zip(clients.keys(), balances)
            }
            set_sheet_with_df(
                workbook, config["worksheet_name"], pd.DataFrame(client_balances)
            )
            await asyncio.sleep(5 * 60)
    finally:
        await asyncio.gather(*[client.close() for client in clients.values()])


if __name__ == "__main__":
    asyncio.run(main())
