import datetime
import logging
from contextlib import suppress
from datetime import timedelta
from random import random
from typing import List, Optional

import ccxt
import devtools
import pendulum
from ccxt.base.exchange import Exchange as CcxtExchange
from click import DateTime
from faker import Faker
from loguru import logger

# from pydantic import BaseModel as _BaseModel
from pydantic import Field, computed_field
from supabase import Client as SupabaseClient
from supabase.client import PostgrestAPIError
from supamodel._abc import BaseModel, IgnoreModel

# from supamodel.commands.handlers import DataHandler
from supamodel._client import client as supabase
from supamodel.enums import Chain, TimeIntSQL

# from supamodel.models.core import BaseModel
from supamodel.trading import market_data
from supamodel.trading.exchange import (
    BaseAsset,
    ChainDefaults,
    Currency,
    CurrencyID,
    ExchangeBase as Exchange,
    ExchangeID,
)
from supamodel.trading.market_data import (  # AssetData,; BaseModel,; Handler,
    Price,
    PriceBar,
    PriceBarInput,
)
from supamodel.utils import memoize_stampede as memoize

fake = Faker()
httpx_logger = logging.getLogger("httpx")
httpx_logger.disabled = True


class SupabaseMeta(BaseModel):

    @property
    def client(self) -> SupabaseClient:
        return supabase

    # add table functions here
    def table(self, table_name: str):
        return self.client.table(table_name)

    def add_records(
        self, table_name: str, data: BaseModel | dict | list[dict]
    ) -> list[dict]:
        try:
            result = self.table(table_name).insert(self.standardize(data)).execute()
            if not result:
                raise ValueError(f"Failed to add records to {table_name}")
            return result.data
        except Exception as e:
            logger.exception(e)
            return []

    def standardize(self, data: list[BaseModel] | BaseModel | dict | list[dict]):
        if isinstance(data, list) and isinstance(data[0], BaseModel):
            return [d.model_dump(mode="json") for d in data]
        if isinstance(data, BaseModel):
            return [data.model_dump(mode="json")]
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list) and isinstance(data[0], dict):
            return data
        return data

    def default_list(self, data):
        return data.data if data else []


class MarketDataClient(BaseModel):
    """
    A client for handling market data.

    This class provides methods for adding bars and prices to the asset OHLCV table.

    Attributes:
        supameta (SupabaseMeta): An instance of the SupabaseMeta class.

    """

    supameta: SupabaseMeta = SupabaseMeta()

    def required(self):
        return set(["supameta"])

    def add_bars(self, asset_data: list[PriceBar] | PriceBar) -> list[dict]:
        """
        Add bars to the asset OHLCV table.

        Args:
            asset_data (AssetData[PriceBar]): The asset data containing price bars.

        Returns:
            list[dict]: A list of dictionaries representing the added records.

        """
        return self.supameta.add_records("asset_ohlcv", asset_data.container_dump())

    def add_prices(self, asset_data: list[Price] | Price):
        """
        Add prices to the asset OHLCV table.

        Args:
            asset_data (AssetData[PriceBar]): The asset data containing price bars.

        """
        return self.supameta.add_records("asset_ohlcv", asset_data.container_dump())

    def default_list(self, data):
        return data.data if data else []

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def between(
        self,
        start: pendulum.datetime,
        end: pendulum.datetime,
        asset_id: str,
    ) -> List[dict]:
        start_iso = start.to_iso8601_string()
        end_iso = end.to_iso8601_string()
        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .between("timestamp", start_iso, end_iso)
            .eq("asset_id", asset_id)
            .execute()
        )
        return self.default_list(result)

    def get_latest_price(self, asset_id: str) -> List[dict]:
        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .eq("asset_id", asset_id)
            .order("timestamp", ascending=False)
            .limit(1)
            .execute()
        )
        return self.default_list(result)

    def get_latest_bar(self, asset_id: str) -> List[dict]:
        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .eq("asset_id", asset_id)
            .order("timestamp", ascending=False)
            .limit(1)
            .execute()
        )
        return self.default_list(result)

    def get_latest_bars(self, asset_id: str, limit: int = 1) -> List[dict]:
        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .eq("asset_id", asset_id)
            .order("timestamp", ascending=False)
            .limit(limit)
            .execute()
        )
        return self.default_list(result)

    def get_latest_prices(self, asset_id: str, limit: int = 1) -> List[dict]:
        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .eq("asset_id", asset_id)
            .order("timestamp", ascending=False)
            .limit(limit)
            .execute()
        )
        return self.default_list(result)

    def multi_latest_bars(
        self, asset_ids: list[str] = [], limit: int = 1
    ) -> List[dict]:
        if not asset_ids:
            return []

        result = (
            self.supameta.table("asset_ohlcv")
            .select("*")
            .in_("asset_id", asset_ids)
            .order("timestamp", ascending=False)
            .limit(limit)
            .execute()
        )
        return self.default_list(result)


def main_price():
    asset_id = "141db0d7-36aa-4bd3-a0fb-05452306ce0c"
    market_data_client = MarketDataClient()
    price_bar = (
        PriceBar(
            address="8ibBBRzj8XbgoaKvRAeomBsXcxRdjj3ZG6vNHDaiczKP",
            type="1m",
            close=0.0001,
            high=0.0001,
            low=0.0001,
            open=0.0001,
            volume=3000000,
            timestamp=pendulum.now(),
        ),
    )
    price = Price(
        address="8ibBBRzj8XbgoaKvRAeomBsXcxRdjj3ZG6vNHDaiczKP",
        price=0.0001,
        timestamp=pendulum.now(),
    )
    # asset_data = AssetData[Price](data=price, asset_id=asset_id)
    # asset_data.asset_id = asset_id
    asset_data = [price]
    resp_data = market_data_client.add_prices(asset_data)
    # asset_data = AssetData[PriceBar](data=price_bar, asset_id=asset_id)
    asset_data.asset_id = asset_id
    resp_data = market_data_client.add_price_bars(asset_data)
    return resp_data
    # print(asset_data.save_dump())


def main():
    # main_asset()
    main_price()


if __name__ == "__main__":
    main()
