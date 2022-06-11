"""
load ccxt using credentials
"""
from dataclasses import dataclass
import ccxt.async_support as ccxt
import yaml

CRED_FILE_LOCATION = "./credentials/account_cred.yml"

@dataclass
class Account:
    exchange_name: str
    market_type: str
    api_key: str
    secret: str
    password: str | None = None
    uid: str | None = None


def get_ccxt_clients_from_yml(
    file_location: str = CRED_FILE_LOCATION,
) -> dict[str, ccxt.Exchange]:
    """
    get ccxt clients from yml file
    """
    with open(file_location, "r") as f:
        yml_data: dict = yaml.safe_load(f)
    clients = {}
    for account_name, cred in yml_data.items():
        account = Account(**cred)
        clients[account_name] = get_ccxt_client(account)
    return clients


def get_ccxt_client(account: Account) -> ccxt.Exchange:
    """
    get ccxt client
    """
    client = getattr(ccxt, account.exchange_name)(
        {
            "apiKey": account.api_key,
            "secret": account.secret,
            "password": account.password,
            "uid": account.uid,
            "enableRateLimit": True,
        }
    )
    return client


if __name__ == "__main__":
    clients = get_ccxt_clients_from_yml()
