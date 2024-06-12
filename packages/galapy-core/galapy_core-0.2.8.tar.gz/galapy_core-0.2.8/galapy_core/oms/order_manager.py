# order_manager.py
from typing import List

from galapy_core.oms.database_manager import DatabaseManager
from galapy_core.oms.exchange_api import ExchangeAPI

from supamodel.enums import OrderSide, OrderStatus
from supamodel.trading.order_management import Order, Trade
from supamodel.trading.portfolio import Position


class OrderManager:
    def __init__(self, exchange_api: ExchangeAPI, db_manager: DatabaseManager):
        self.exchange_api = exchange_api
        self.db_manager = db_manager

    def submit_order(self, order: Order) -> Order:
        # Submit the order to the exchange
        exchange_order = self.exchange_api.submit_order(order)

        # Save the order to the database
        saved_order = self.db_manager.save_order(exchange_order)

        return saved_order

    def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        # Update the order status in the database
        updated_order = self.db_manager.change_order_status(order_id, status)

        return updated_order

    def process_order(self, order: Order) -> Trade:
        # Create or update the position based on the order
        position = self.db_manager.create_position(order)

        # Create a trade record
        trade = Trade(
            position_id=position.id,
            order_id=order.id,
            quantity=order.quantity,
            price=order.price,
            fee=self.exchange_api.calculate_fee(order),
            timestamp=self.exchange_api.get_fill_timestamp(order),
        )

        # Save the trade to the database
        saved_trade = self.db_manager.save_trade(trade)

        return saved_trade

    def update_position(self, order: Order, trade: Trade) -> Position:
        # Retrieve the position from the database
        position = self.db_manager.get_position(trade.position_id)

        # Update the position based on the order and trade details
        fill_quantity, fill_price = self.exchange_api.get_fill_details(order)
        if order.side == OrderSide.BUY:
            position.quantity += fill_quantity
            position.average_price = fill_price
        else:
            position.quantity -= fill_quantity

        # Save the updated position to the database
        updated_position = self.db_manager.save_position(position)

        return updated_position

    def check_open_orders(self) -> None:
        # Retrieve open orders from the database
        open_orders = self.db_manager.get_open_orders_from_db()

        for order in open_orders:
            # Retrieve the order from the exchange
            exchange_order = self.exchange_api.get_order(order.id)

            # Check the order status
            if exchange_order.status in [
                OrderStatus.FILLED,
                OrderStatus.PARTIALLY_FILLED,
            ]:
                # Process the order and update the position
                trade = self.process_order(exchange_order)
                self.update_position(exchange_order, trade)
                self.update_order_status(order.id, exchange_order.status)
            elif exchange_order.status == OrderStatus.CANCELED:
                # Update the order status in the database
                self.update_order_status(order.id, OrderStatus.CANCELED)
            elif exchange_order.status == OrderStatus.REJECTED:
                # Update the order status in the database
                self.update_order_status(order.id, OrderStatus.REJECTED)
