import logging
from contextlib import suppress
from typing import List, Optional

import ccxt
import devtools
import pendulum
from ccxt.base.exchange import Exchange as CcxtExchange
from loguru import logger
from supabase.client import PostgrestAPIError
from supamodel._abc import BaseModel, IgnoreModel
from supamodel._client import client as supabase
from supamodel.enums import Chain
from supamodel.trading.exchange import (
    Asset,
    BaseAsset,
    ChainAsset,
    ChainDefaults,
    Currency,
    CurrencyID,
    ExchangeBase as Exchange,
    ExchangeID,
)
from supamodel.trading.tokens import AssetOverview

httpx_logger = logging.getLogger("httpx")
httpx_logger.disabled = True


DEFAULTS = {
    Chain.SOLANA: ChainDefaults(
        **{
            "exchanges": ["raydium", "jupiter", "orca", "serum"],
            "currencies": [
                {"code": "USDC", "name": "USD Coin"},
                {"code": "wSOL", "name": "Wrapped Solana"},
                {"code": "SOL", "name": "Solana"},
                {"code": "USDT", "name": "Tether USD"},
            ],
            "default_exchange": "raydium",
            "default_currency": "SOL",
        }
    ),
    # Chain.ETHEREUM: 'uniswap'
}
ASSET_CLIENT: Optional["AssetClient"] = None


# ---------------------------------------------------------
# Classes
# ---------------------------------------------------------


class LocalAssetData(BaseModel):
    exchange_ids: List[ExchangeID] = []
    currency_ids: List[CurrencyID] = []

    def get_local_exchange_id(self, exchange_name: str) -> str | None:
        for exchange in self.exchange_ids:
            if exchange.name == exchange_name:
                return exchange.exchange_id
        return None

    def get_local_currency_id(self, code: str) -> str | None:
        for currency in self.currency_ids:
            if currency.code == code:
                return currency.currency_id
        return None

    def add_local_exchange_id(
        self, exchange_id: str | None, exchange_name: str
    ) -> bool:
        if not exchange_id:
            return False
        self.exchange_ids.append(
            ExchangeID(exchange_id=exchange_id, name=exchange_name)
        )
        return True

    def add_currency_id(self, currency_id: str | None, currency: Currency) -> bool:
        if not currency_id:
            return False
        self.currency_ids.append(
            CurrencyID(currency_id=currency_id, code=currency.code, name=currency.name)
        )
        return True


class AssetClient(BaseModel):
    local_data: LocalAssetData = LocalAssetData()

    # exchange_ids: list[ExchangeID] = []
    # currency_ids: list[CurrencyID] = []
    @property
    def exchange_ids(self):
        return self.local_data.exchange_ids

    @exchange_ids.setter
    def exchange_ids(self, value: ExchangeID):
        self.local_data.exchange_ids.append(value)

    @property
    def currency_ids(self):
        return self.local_data.currency_ids

    @currency_ids.setter
    def currency_ids(self, value: CurrencyID):
        return self.local_data.currency_ids.append(value)

    @property
    def asset_logic(self):
        return AssetLogic(client=self)

    def _get_local_exchange_id(self, exchange_name: str) -> str | None:
        for exchange in self.exchange_ids:
            if exchange.name == exchange_name:
                return exchange.exchange_id
        return None

    def get_local_currency_id(self, code: str) -> str | None:
        for currency in self.currency_ids:
            if currency.code == code:
                return currency.currency_id
        return None

    def _add_local_exchange_id(
        self, exchange_id: str | None, exchange_name: str
    ) -> bool:
        if not exchange_id:
            return False
        self.exchange_ids.append(
            ExchangeID(exchange_id=exchange_id, name=exchange_name)
        )
        return True

    def _add_local_currency_id(
        self, currency_id: str | None, currency: Currency
    ) -> bool:
        if not currency_id:
            return False

        self.currency_ids.append(
            CurrencyID(currency_id=currency_id, code=currency.code, name=currency.name)
        )
        return True

    def get_exchange_id(self, exchange_name: str) -> str | None:

        local_exchange_id = (
            self._get_local_exchange_id(exchange_name)
            if bool(self.exchange_ids)
            else None
        )
        if local_exchange_id:
            return local_exchange_id
        exchange_data = get_exchange(exchange_name)
        if exchange_data:
            first_exchange = exchange_data[0]
            return first_exchange.get("id", None)
        return None

    def get_currency_id(self, code: str) -> str | None:

        local_id = self.get_local_currency_id(code)
        if local_id:
            return local_id
        currency_data = get_currency(code)
        if currency_data:
            first_currency = currency_data[0]
            return first_currency.get("id", None)
        return None

    def add_exchange(self, exchange: Exchange) -> str | None:
        exchange_result = add_exchange(
            name=exchange.name,
            description=exchange.description,
            maker_fee=exchange.maker_fee,
            taker_fee=exchange.taker_fee,
            url=exchange.url,
        )
        exchange_result = exchange_result

        if isinstance(exchange_result, dict) and exchange_result.get("id", None):
            exchange_id = exchange_result.get("id")
            return exchange_id

        logger.error("Failed to add exchange")
        return None

    def add_currency(self, currency: Currency) -> str | None:
        result_data = add_currency(currency.code, currency.name)
        if not result_data:
            return None
        return result_data[0].get("id", None)

    def add_asset(self, asset: BaseAsset) -> dict | None:
        return self.asset_logic.add_asset(asset)

    def init_defaults(self, chain: Chain):
        defaults = DEFAULTS.get(chain, None)
        if not defaults:
            return None

        self.init_exchange_defaults(chain, defaults)
        self.init_currency_defaults(chain, defaults)

    def init_exchange_defaults(self, chain: Chain, defaults: ChainDefaults):
        for exchange in defaults.exchanges:
            exchange_id = self.get_exchange_id(exchange)
            if exchange_id:
                # exchange_container = ExchangeID(name=exchange, exchange_id=exchange_id)

                self.exchange_ids.append(
                    ExchangeID(name=exchange, exchange_id=exchange_id)
                )
                continue
            exchange_id = self.add_exchange(
                Exchange(
                    name=exchange,
                    description=f"{exchange} is a popular cryptocurrency exchange for {chain.value.capitalize()}.",
                    maker_fee=0.0001,
                    taker_fee=0.0001,
                )
            )
            if exchange_id:
                self.exchange_ids.append(
                    ExchangeID(name=exchange, exchange_id=exchange_id)
                )

    def init_currency_defaults(self, chain: Chain, defaults: ChainDefaults):
        for currency in defaults.currencies:
            self.get_or_add_currency(currency)

    def get_or_add_currency(self, currency: Currency):
        currency_id = self.get_currency_id(currency.code)
        if self.local_data.add_currency_id(currency_id, currency):
            logger.info(
                f"Currency {currency.code} already exists with ID {currency_id}"
            )
            return currency_id

        currency_id = self.add_currency(currency)
        if not self.local_data.add_currency_id(currency_id, currency):
            raise ValueError(f"Currency Wasn't Added, Code: {currency.code}")

        logger.info(f"Added currency {currency.code} with ID {currency_id}")
        return currency_id

    def get_add_asset(self, asset: BaseAsset) -> dict | None:
        return self.asset_logic.get_add_asset(asset)

    def find_asset_id_by_address(self, address: str) -> str | None:
        return self.asset_logic.get_by_address(address)

    def get_by_asset(self, asset: BaseAsset) -> dict | None:
        return self.asset_logic.get_asset(asset)

    def meme_coins(self):
        coins = self.asset_logic.meme_coins()
        return [ChainAsset(**coin) for coin in coins]


class AssetLogic(IgnoreModel):
    asset: BaseAsset | None = None
    client: AssetClient
    exchange_cache: dict[str, dict] = {
        "by_name": {},
        "by_id": {},
    }
    currency_cache: dict[str, dict] = {
        "by_code": {},
        "by_id": {},
    }

    def check_exchange_cache(self, exchange_name: str) -> dict | None:
        return self.exchange_cache.get("by_name").get(exchange_name, None)

    def check_currency_cache(self, currency_code: str) -> dict | None:
        return self.currency_cache.get("by_code").get(currency_code, None)

    def add_exchange_cache(self, exchange_data: dict):
        exchange_id = exchange_data.get("id")
        exchange_name = exchange_data.get("name")
        self.exchange_cache["by_name"][exchange_name] = exchange_data
        self.exchange_cache["by_id"][exchange_id] = exchange_data

    def is_chain(self) -> bool:
        return isinstance(self.asset, ChainAsset)

    def is_normal(self) -> bool:
        return isinstance(self.asset, Asset)

    def defaults(self, chain: Chain):
        return DEFAULTS.get(chain, None)

    def add_chain(self):
        # if self.is_chain():
        chain = Chain(self.asset.chain)
        defaults = self.defaults(chain)
        if not defaults:
            raise ValueError("Chain not found in defaults")
        default_exchange = self.asset.exchange or defaults.default_exchange
        default_currency = defaults.default_currency
        exchange_id = self.client.get_exchange_id(default_exchange)
        base_id = self.client.get_currency_id(default_currency)
        trade_id = self.client.get_or_add_currency(
            Currency(code=self.asset.symbol, name=self.asset.name)
        )
        self.asset.base_currency_id = base_id
        self.asset.trade_currency_id = trade_id
        self.asset.exchange_id = exchange_id
        return self.asset.supa_dump()

    def get_exchange_id(self):
        cache_obj = self.check_exchange_cache(self.asset.exchange)
        if cache_obj:
            return cache_obj.get("id")
        exchange_id = self.client.get_exchange_id(self.asset.exchange)
        self.add_exchange_cache({"id": exchange_id, "name": self.asset.exchange})
        if not exchange_id:
            raise ValueError("Exchange not found")
        return exchange_id

    def get_currency_id(self, code: str):
        cache_obj = self.check_currency_cache(code)
        if cache_obj:
            return cache_obj.get("id")
        _id = self.client.get_currency_id(code)
        if not _id:
            raise ValueError("Currency not found")
        self.currency_cache["by_code"][code] = {"id": _id, "code": code}
        return _id

    def add_normal(self):

        exchange_id = self.get_exchange_id(self.asset.exchange)
        base_id = self.get_currency_id(self.asset.base)
        trade_id = self.get_currency_id(self.asset.trade)
        if not exchange_id or not base_id or not trade_id:
            raise ValueError("Currency or exchange not found")
        self.asset.base_currency_id = base_id
        self.asset.trade_currency_id = trade_id
        self.asset.exchange_id = exchange_id
        return self.asset.supa_dump()

    def add_asset(self, asset: BaseAsset | None = None):
        usable_asset = asset or self.asset
        self.asset = usable_asset
        asset_dump = self.add_normal() if not self.is_chain() else self.add_chain()

        try:
            result = supabase.table("assets").insert(asset_dump).execute()
            data = result.data
            if not data:
                raise ValueError("Failed to add asset")
            asset_dict = data[0]
            logger.success(f"Added Asset: {asset_dict.get('name')}")
            return asset_dict
        except PostgrestAPIError as pst_e:
            if pst_e.code == "23505":
                logger.error("Asset Already Exists")
            else:
                logger.exception(pst_e)

        except ValueError as ve:
            logger.exception(ve)
        except Exception as e:
            raise e
        return None

    def get_asset(self, asset: BaseAsset):
        usable_asset = asset or self.asset
        self.asset = usable_asset
        asset_dump = self.add_normal() if not self.is_chain() else self.add_chain()
        base_id = asset_dump.get("base_currency_id")
        trade_id = asset_dump.get("trade_currency_id")
        exchange_id = asset_dump.get("exchange_id")
        asset_select = get_asset(exchange_id, base_id, trade_id)
        if asset_select:
            return asset_select
        return None

    def get_asset_id(self, asset: BaseAsset):
        asset_data = self.get_asset(asset)
        if not asset_data:
            return None
        return asset_data.get("id")

    def get_add_asset(self, asset: BaseAsset):
        asset_data = self.get_asset(asset)
        if not asset_data:
            return self.add_asset(asset)
        return asset_data

    def get_by_address(self, address: str):
        asset_id = find_asset_id_by_address(address)
        if asset_id:
            return asset_id
        return None

    def meme_coins(self):
        return get_meme_assets()


# ---------------------------------------------------------
# Global Accessors
# ---------------------------------------------------------


def get_asset_client() -> AssetClient:
    global ASSET_CLIENT
    if not ASSET_CLIENT:
        ASSET_CLIENT = AssetClient()
    return ASSET_CLIENT


def get_ccxt_exchanges():
    exchange_names = ccxt.exchanges
    return exchange_names


# @memoize(expire=0.5)
def get_currency(code: str):
    currency = supabase.table("currencies").select("*").eq("code", code).execute()
    return currency.data


# @memoize(expire=0.2)
def get_exchange(name: str):
    """
    Retrieves exchange data from the 'exchanges' table based on the provided name.

    Args:
        name (str): The name of the exchange.

    Returns:
        dict: The exchange data retrieved from the 'exchanges' table.
    """
    exchange = supabase.table("exchanges").select("*").eq("name", name).execute()
    if not exchange:
        return None
    return exchange.data


# @memoize(expire=2)
def get_asset(exchange_id: str, base_id: str, trade_id: str):
    asset = (
        supabase.table("assets")
        .select("*")
        .eq("exchange_id", exchange_id)
        .eq("base_currency_id", base_id)
        .eq("trade_currency_id", trade_id)
        .execute()
    )
    data = asset.data
    if data:
        return data[0]
    return None


def add_exchange(
    name: str, description: str, maker_fee: float, taker_fee: float, url: str
):
    input_data = {
        "name": name,
        "description": description,
        "maker_fee": maker_fee,
        "taker_fee": taker_fee,
        "url": url,
    }
    # Filter none values
    input_data = {k: v for k, v in input_data.items() if v is not None}
    with suppress(Exception):
        result = supabase.table("exchanges").insert(input_data).execute()
        # if not result:
        #     return None
        data = result.data
        if data:
            return data[0]
    return None
    # logger.info(data)


def add_ccxt_exchange(exchange: CcxtExchange):
    fees = exchange.fees["trading"]
    maker = fees.get("maker")
    taker = fees.get("taker")
    www_url = exchange.urls.get("www")
    with suppress(Exception):
        exchange = add_exchange(
            exchange.name,
            f"{exchange.name} is a popular cryptocurrency exchange.",
            maker,
            taker,
            www_url,
        )
        devtools.debug(exchange)
        return True
    return False


def add_currency(currency: str, name: str = None):
    with suppress(Exception):
        result = (
            supabase.table("currencies")
            .insert({"code": currency, "name": name})
            .execute()
        )
        if not result:
            return None
        return result.data
        # devtools.debug(result)
        # return True
    return None


def add_asset(name, base_id, trade_id, exchange_id):
    if not base_id or not trade_id or not exchange_id:
        raise ValueError("Currency or exchange not found")
    input_data = {
        "name": name,
        "base_currency_id": base_id,
        "trade_currency_id": trade_id,
        "exchange_id": exchange_id,
    }
    result = supabase.table("assets").insert(input_data).execute()
    data = result.data
    logger.info(data)


def add_price(asset_id: str, price: str, timestamp: pendulum.datetime):
    input_data = {
        "asset_id": asset_id,
        "price": price,
        "timestamp": timestamp.to_iso8601_string(),
    }
    result = supabase.table("asset_prices").insert(input_data).execute()
    data = result.data
    logger.info(data)


def add_batch_prices(prices: list[dict]):

    result = supabase.table("asset_prices").insert(prices).execute()
    data = result.data
    logger.info(data)


def add_ohlcv(
    asset_id: str,
    open: str,
    high: str,
    low: str,
    close: str,
    volume: str,
    timestamp: pendulum.datetime,
):
    input_data = {
        "asset_id": asset_id,
        "open": open,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
        "timestamp": timestamp.to_iso8601_string(),
    }
    result = supabase.table("ohlcv").insert(input_data).execute()
    data = result.data
    logger.info(data)


def find_asset_id_by_address(address: str) -> str | None:
    asset = supabase.table("assets").select("*").eq("address", address).execute()
    data = asset.data
    if data:
        return data[0].get("id")
    return None


def get_meme_assets():
    assets = supabase.table("assets").select("*").eq("is_meme", True).execute()
    data = assets.data
    if data:
        return data
    return None


def add_batch_ohlcv(ohlcv: list[dict]):
    result = supabase.table("ohlcv").insert(ohlcv).execute()
    data = result.data
    logger.info(data)


def create_asset_from_overview(overview: AssetOverview):
    asset = ChainAsset(
        name=overview.name,
        chain=Chain.SOLANA,
        symbol=overview.symbol,
        decimals=overview.decimals,
        is_meme=overview.is_meme,
        address=overview.address,
        # base=overview.base,
        # trade=overview.trade,
        # exchange=overview.exchange,
    )
    return asset


def main():
    asset_client = AssetClient()
    asset_client.init_defaults(Chain.SOLANA)
    asset = ChainAsset(
        name="Snack Wrap",
        symbol="SNKWRP",
        address="8ibBBRzj8XbgoaKvRAeomBsXcxRdjj3ZG6vNHDaiczKP",
        # exchange="orca",
        decimals=9,
        chain=Chain.SOLANA,
    )
    asset_dict = asset_client.get_add_asset(asset=asset)
    logger.warning(asset_dict.get("id"))


if __name__ == "__main__":
    main()
