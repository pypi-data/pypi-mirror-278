import contextlib
import random
from datetime import datetime
from typing import List

import pendulum
from postgrest._sync.request_builder import SyncRequestBuilder
from postgrest.base_request_builder import APIResponse
from rich import print
from supabase.client import PostgrestAPIError

from supamodel._client import client as supabase
from supamodel._logging import logger
from supamodel.enums import OrderSide, OrderStatus, OrderType
from supamodel.exceptions import EmptyResponseError
from supamodel.trading.order_management import Order, Trade
from supamodel.trading.portfolio import Portfolio, Position

# Can get the exchange_id from the asset_id. We can simply look at the asset's exchange_id and return it.

depth_logger = logger.opt(depth=1)


class MockExchangeAPI:
    """
    A mock implementation of an exchange API.

    This class provides methods to simulate order submission, retrieval, fee calculation,
    and other exchange-related operations.

    Methods:
        submit_order(order: Order) -> Order:
            Submits an order and returns the filled order.

        get_order(order_id: str) -> Order:
            Retrieves an order based on the given order ID.

        calculate_fees(order: Order) -> float:
            Calculates the fees for the given order.

        get_exchange_id(asset_id: str) -> str:
            Retrieves the exchange ID for the given asset ID.

        get_current_price(position: Position) -> float:
            Retrieves the current price for the given position.

        get_fill_timestamp(order: Order) -> float:
            Retrieves the fill timestamp for the given order.

        get_fill_details(order: Order) -> dict:
            Retrieves the fill details for the given order.

        calculate_fee(order: Order) -> float:
            Calculates the fee for the given order.
    """

    def submit_order(self, order: Order) -> Order:
        """
        Submits an order and updates its status to FILLED.

        Args:
            order (Order): The order to be submitted.

        Returns:
            Order: The submitted order with the updated status.
        """
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
        """
        Get the fill timestamp for the given order.

        Parameters:
            order (Order): The order for which to get the fill timestamp.

        Returns:
            float: The fill timestamp in UTC.
        """
        return pendulum.now("UTC").timestamp()

    def get_fill_details(self, order: Order) -> dict:
        return random.uniform(0.1, 100), random.uniform(0.1, 8.0)

    def calculate_fee(self, order: Order) -> float:
        return random.uniform(0.0, 0.1)


exchange_api = MockExchangeAPI()


def save_order(order: Order) -> Order:
    """
    Submits an order to the database.

    Args:
        order (Order): The order to be submitted.

    Returns:
        Order: The submitted order.

    Raises:
        EmptyResponseError: If the response from the database is empty.
    """
    response = supabase.table("orders").insert(order.supa_dump(by_alias=True)).execute()
    resp_data = response.data
    resp_data if resp_data else []
    if not resp_data:
        raise EmptyResponseError("Failed to add order to the database.")

    return Order(**resp_data[0])


def change_order_status(order_id: str, status: OrderSide) -> Order:
    """
    Change the status of an order.

    Args:
        order_id (str): The ID of the order to update.
        status (OrderSide): The new status of the order.

    Returns:
        Order: The updated order object.

    """
    result = (
        supabase.table("orders")
        .update({"status": status.value})
        .eq("id", order_id)
        .execute()
    )
    results = process_results(result)
    return Order(**results[0])
    # return resp_data


def get_position_by_portfolio_asset_id(
    portfolio_id: str, asset_id: str
) -> Position | None:
    result: APIResponse = (
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


def create_position(order: Order, by_alias: bool = False) -> Position:
    """
    Creates a new position based on the given order and saves it to the database.

    Args:
        order (Order): The order object containing the details of the position.

    Returns:
        Position: The newly created position object.

    """

    new_position = Position(
        portfolio_id=order.portfolio_id,
        asset_id=order.asset_id,
        quantity=order.quantity,
        average_price=order.price,
    )
    existing_position = get_position_by_portfolio_asset_id(
        order.portfolio_id, order.asset_id
    )
    if not existing_position:
        result: APIResponse = (
            supabase.table("positions")
            .insert(new_position.supa_dump(by_alias=by_alias))
            .execute()
        )
        results = process_results(result)

        return Position(**results[0])
    new_position.id = existing_position.id
    result: APIResponse = (
        supabase.table("positions")
        .upsert(new_position.supa_dump(by_alias=by_alias))
        .execute()
    )
    results = process_results(result)

    return Position(**results[0])


def process_results(results: APIResponse, need_data: bool = True) -> List[dict]:
    """
    Process the results from the API response.

    Args:
        results (APIResponse): The API response object.
        need_data (bool, optional): Flag indicating whether data is required. Defaults to True.

    Returns:
        List[dict]: The processed result data.

    Raises:
        EmptyResponseError: If the result data is empty and need_data is True.
    """
    result_data = results.data if results.data else []
    if not result_data and need_data:
        depth_logger.error("Failed to process Supabase results.")
        raise EmptyResponseError()

    return result_data


def transact_trade_position(order: Order) -> Trade:
    # with contextlib.suppress(Exception):
    position: Position = create_position(order)

    trade = Trade(
        position_id=position.id,
        order_id=order.id,
        quantity=order.quantity,
        price=order.price,
        fee=exchange_api.calculate_fee(order),
        timestamp=exchange_api.get_fill_timestamp(order),
    )
    result = supabase.table("trades").insert(trade.supa_dump(by_alias=True)).execute()

    results = process_results(result)
    return Trade(**results[0])


# @retry(exception=PostgrestAPIError, tries=5, delay=1)
def get_position(position_id: str) -> Position:
    result = supabase.table("positions").select("*").eq("id", position_id).execute()
    results = process_results(result)
    return Position(**results[0])


def save_position(position: Position, by_alias=False) -> Position:
    result = (
        supabase.table("positions")
        .update(position.supa_dump(by_alias=by_alias))
        .eq("id", position.id)
        .execute()
    )
    results = process_results(result)
    return Position(**results[0])


def update_position(order: Order, trade: Trade) -> Position:
    position = get_position(trade.position_id)
    fill_quantity, fill_price = exchange_api.get_fill_details(order)
    if order.side == OrderSide.BUY:
        position.quantity += fill_quantity
        position.average_price = fill_price
    else:
        position.quantity -= fill_quantity
    position.updated_at = datetime.now()
    return save_position(position)


def get_open_orders_from_db() -> List[Order]:
    query = (
        supabase.table("orders")
        .select("*")
        .in_("status", [OrderStatus.PENDING.value, OrderStatus.PARTIALLY_FILLED.value])
    )
    response = query.execute()
    if response.data:
        return [Order(**order_data) for order_data in response.data]
    return []


def check_open_orders():
    # Retrieve all open orders from the database
    open_orders = get_open_orders_from_db()

    for order in open_orders:
        order_id = order.id

        # Retrieve the order from the exchange using the order_id
        exchange_order = exchange_api.get_order(order_id)

        # Check the order status
        if exchange_order.status in [OrderStatus.FILLED, OrderStatus.PARTIALLY_FILLED]:
            # Order is filled, process the trade and update position
            trade = transact_trade_position(exchange_order)
            update_position(exchange_order, trade)
            change_order_status(order_id, exchange_order.status)
        elif exchange_order.status == OrderStatus.CANCELED:
            # Order is canceled, update the order status in the database
            change_order_status(order_id, OrderStatus.CANCELED)
        elif exchange_order.status == OrderStatus.REJECTED:
            # Order is rejected, update the order status in the database
            change_order_status(order_id, OrderStatus.REJECTED)
        else:
            # Order is still pending or partially filled, no action needed
            continue


def main():
    #
    portfolio_json = [
        {
            "id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "user_id": "b3209dcc-3097-430e-8ad1-c9bb4660aa4c",
            "name": "USD Portfolio",
            "exchange_id": "6663abed-f538-40ad-9ebc-8aa183944b34",
            "base_currency_id": "0cef4f9b-d607-408e-92ed-5a0382e0fe35",
            "created_at": pendulum.DateTime.now().subtract(days=3),
            "updated_at": pendulum.DateTime.now(),
            "balance": "186205.7935856367730908",
        }
    ]
    man_portfolio = Portfolio(**portfolio_json[0])
    [
        {
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "quantity": "95.18501283",
            "average_price": "370.86070974",
            "created_at": "2024-04-09 06:06:18.065308+00",
            "updated_at": "2024-04-09 06:06:18.065308+00",
        }
    ]
    man_position = Position(
        **{
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "quantity": "95.18501283",
            "average_price": "370.86070974",
            "created_at": pendulum.DateTime.now().subtract(days=2),
            "updated_at": pendulum.DateTime.now(),
        }
    )
    man_order = Order(
        **{
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "exchange_id": "6663abed-f538-40ad-9ebc-8aa183944b34",
            "order_type": OrderType.MARKET,
            "side": OrderSide.BUY,
            "quantity": 10,
            "price": 100,
            "status": OrderStatus.PENDING,
            "created_at": pendulum.DateTime.now().subtract(days=1),
            "updated_at": pendulum.DateTime.now(),
        }
    )
    print(man_portfolio)
    print(man_position)
    print(man_order)

    # print(manual)

    # manual_order = Order(
    #     asset_id=manual.asset_id,
    #     portfolio_id=portfolio.id,
    #     quantity=10,
    #     price=100,
    #     side=OrderSide.BUY,
    #     type=OrderType.MARKET,
    # )
    # print(manual_order)


if __name__ == "__main__":
    main()
