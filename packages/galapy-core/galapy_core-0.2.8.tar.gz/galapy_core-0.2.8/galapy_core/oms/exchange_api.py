# exchange_api.py
import abc
import random
from typing import List

import pendulum

from supamodel.enums import OrderSide, OrderStatus, OrderType
from supamodel.trading.order_management import Order, Trade
from supamodel.trading.portfolio import Position


class ExchangeAPI(abc.ABC):
    @abc.abstractmethod
    def submit_order(self, order: Order) -> Order:
        pass

    @abc.abstractmethod
    def get_order(self, order_id: str) -> Order:
        pass

    @abc.abstractmethod
    def calculate_fees(self, order: Order) -> float:
        pass

    @abc.abstractmethod
    def get_exchange_id(self, asset_id: str) -> str:
        pass

    @abc.abstractmethod
    def get_current_price(self, position: Position) -> float:
        pass

    @abc.abstractmethod
    def get_fill_timestamp(self, order: Order) -> float:
        pass

    @abc.abstractmethod
    def get_fill_details(self, order: Order) -> dict:
        pass

    @abc.abstractmethod
    def calculate_fee(self, order: Order) -> float:
        pass


class MockExchangeAPI(ExchangeAPI):
    def submit_order(self, order: Order) -> Order:
        order.status = OrderStatus.FILLED
        return order

    def get_order(self, order_id: str) -> Order:
        return Order()

    def calculate_fees(self, order: Order) -> float:
        return random.uniform(0.0, 0.1)

    def get_exchange_id(self, asset_id: str) -> str:
        return "exchange_id"

    def get_current_price(self, position: Position) -> float:
        return random.uniform(0.0, 100.0)

    def get_fill_timestamp(self, order: Order) -> float:
        return pendulum.now("UTC").timestamp()

    def get_fill_details(self, order: Order) -> dict:
        return random.uniform(0.1, 100), random.uniform(0.1, 8.0)

    def calculate_fee(self, order: Order) -> float:
        return random.uniform(0.0, 0.1)
