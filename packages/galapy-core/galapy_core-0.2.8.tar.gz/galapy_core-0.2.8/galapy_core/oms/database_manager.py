# database_manager.py
import abc
from typing import List

from supamodel import logger, print, supabase_client as supabase
from supamodel.enums import OrderStatus
from supamodel.exceptions import EmptyResponseError
from supamodel.trading.order_management import Order, Trade
from supamodel.trading.portfolio import Position


class DatabaseManager(abc.ABC):
    @abc.abstractmethod
    def save_order(self, order: Order) -> Order:
        pass

    @abc.abstractmethod
    def change_order_status(self, order_id: str, status: OrderStatus) -> Order:
        pass

    @abc.abstractmethod
    def get_position_by_portfolio_asset_id(
        self, portfolio_id: str, asset_id: str
    ) -> Position:
        pass

    @abc.abstractmethod
    def create_position(self, order: Order, by_alias: bool = False) -> Position:
        pass

    @abc.abstractmethod
    def get_position(self, position_id: str) -> Position:
        pass

    @abc.abstractmethod
    def save_position(self, position: Position, by_alias=False) -> Position:
        pass

    @abc.abstractmethod
    def get_open_orders_from_db(self) -> List[Order]:
        pass

    @abc.abstractmethod
    def get_trades(self) -> List[Trade]:
        pass

    @abc.abstractmethod
    def get_orders(self) -> List[Order]:
        pass

    @abc.abstractmethod
    def get_positions(self) -> List[Position]:
        pass


class SupabaseDatabaseManager(DatabaseManager):
    def save_order(self, order: Order) -> Order:
        response = (
            supabase.table("orders").insert(order.supa_dump(by_alias=True)).execute()
        )
        resp_data = response.data
        resp_data if resp_data else []
        if not resp_data:
            raise Exception("Failed to add order to the database.")
            # raise EmptyResponseError("Failed to add order to the database.")
        return Order(**resp_data[0])

    def change_order_status(self, order_id: str, status: OrderStatus) -> Order:
        result = (
            supabase.table("orders")
            .update({"status": status.value})
            .eq("id", order_id)
            .execute()
        )
        results = self._process_results(result)
        return Order(**results[0])

    def get_position_by_portfolio_asset_id(
        self, portfolio_id: str, asset_id: str
    ) -> Position:
        result = (
            supabase.table("positions")
            .select("*")
            .eq("portfolio_id", portfolio_id)
            .eq("asset_id", asset_id)
            .limit(1)
            .execute()
        )
        if result.data:
            return Position(**result.data[0])
        return None

    def create_position(self, order: Order, by_alias: bool = False) -> Position:
        new_position = Position(
            portfolio_id=order.portfolio_id,
            asset_id=order.asset_id,
            quantity=order.quantity,
            average_price=order.price,
        )
        existing_position = self.get_position_by_portfolio_asset_id(
            order.portfolio_id, order.asset_id
        )
        if not existing_position:
            result = (
                supabase.table("positions")
                .insert(new_position.supa_dump(by_alias=by_alias))
                .execute()
            )
            results = self._process_results(result)
            return Position(**results[0])
        new_position.id = existing_position.id
        result = (
            supabase.table("positions")
            .upsert(new_position.supa_dump(by_alias=by_alias))
            .execute()
        )
        results = self._process_results(result)
        return Position(**results[0])

    def get_position(self, position_id: str) -> Position:
        result = supabase.table("positions").select("*").eq("id", position_id).execute()
        results = self._process_results(result)
        return Position(**results[0])

    def save_position(self, position: Position, by_alias=False) -> Position:
        result = (
            supabase.table("positions")
            .update(position.supa_dump(by_alias=by_alias))
            .eq("id", position.id)
            .execute()
        )
        results = self._process_results(result)
        return Position(**results[0])

    def get_open_orders_from_db(self) -> List[Order]:
        query = (
            supabase.table("orders")
            .select("*")
            .in_(
                "status",
                [OrderStatus.PENDING.value, OrderStatus.PARTIALLY_FILLED.value],
            )
        )
        response = query.execute()
        if response.data:
            return [Order(**order_data) for order_data in response.data]
        return []

    def _process_results(self, results, need_data: bool = True) -> List[dict]:
        result_data = results.data if results.data else []
        if not result_data and need_data:
            logger.warning("Supabase returned an empty response.")
        return result_data

    def save_trade(self, trade: Trade, by_alias: bool = False) -> Trade:
        response = (
            supabase.table("trades")
            .insert(trade.supa_dump(by_alias=by_alias))
            .execute()
        )
        resp_data = response.data
        resp_data if resp_data else []
        if not resp_data:
            raise Exception("Failed to add trade to the database.")
        return Trade(**resp_data[0])

    def get_trades(self) -> List[Trade]:
        result = supabase.table("trades").select("*").execute()
        results = self._process_results(result)
        return [Trade(**trade_data) for trade_data in results]

    def get_orders(self) -> List[Order]:
        result = supabase.table("orders").select("*").execute()
        results = self._process_results(result)
        return [Order(**order_data) for order_data in results]

    def get_positions(self) -> List[Position]:
        result = supabase.table("positions").select("*").execute()
        results = self._process_results(result)
        return [Position(**position_data) for position_data in results]

    def get_open_orders(self) -> List[Order]:
        result = (
            supabase.table("orders")
            .select("*")
            .in_(
                "status",
                [OrderStatus.PENDING.value],
            )
            .execute()
        )
        results = self._process_results(result)
        return [Order(**order_data) for order_data in results]

    def get_orders_params(
        self, status: OrderStatus | None = None, portfolio_id: str | None = None
    ) -> List[Order]:
        query = supabase.table("orders").select("*")
        if status:
            query = query.eq("status", status.value)
        if portfolio_id:
            query = query.eq("portfolio_id", portfolio_id)
        result = query.execute()

        results = self._process_results(result)
        return [Order(**order_data) for order_data in results]
