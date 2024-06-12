import random
from datetime import datetime
from typing import List

import pendulum
from pydantic import BaseModel
from rich import print
from supabase.client import Client
from supamodel._client import client as supabase
from supamodel._logging import devtools, logger

from galapy_core.generators import PriceGenerator

supabase: Client = supabase


class PortfolioClient(BaseModel):
    pass


def get_all_users():
    """Get all users from the database.

    Returns:
        list: A list of all users.
    """
    return supabase.auth.admin.list_users()


def user_ids() -> list[str]:
    users = get_all_users()
    return [user.id for user in users]


def select_user_id() -> str:
    users = user_ids()
    return random.choice(users)


def create_portfolio(user_id: str, base_currency_code: str, exchange_name: str):
    # Retrieve exchange_id
    exchange_data = (
        supabase.table("exchanges").select("id").eq("name", exchange_name).execute()
    )
    if not exchange_data.data:
        return {"error": f"Exchange '{exchange_name}' not found."}
    exchange_id = exchange_data.data[0]["id"]

    # Retrieve base_currency_id
    currency_data = (
        supabase.table("currencies")
        .select("id")
        .eq("code", base_currency_code)
        .execute()
    )
    if not currency_data.data:
        return {"error": f"Base currency '{base_currency_code}' not found."}
    base_currency_id = currency_data.data[0]["id"]

    # Check if the exchange has assets with the specified base currency
    if not check_exchange_assets(exchange_name, base_currency_code):
        return {
            "error": f"Exchange '{exchange_name}' does not have assets with base currency '{base_currency_code}'."
        }

    # Insert new portfolio
    new_portfolio = (
        supabase.table("portfolios")
        .insert(
            {
                "user_id": user_id,
                "name": f"{base_currency_code} Portfolio",
                "exchange_id": exchange_id,
                "base_currency_id": base_currency_id,
            }
        )
        .execute()
    )

    if new_portfolio.data:
        return {"success": True, "portfolio_id": new_portfolio.data[0]["id"]}
    else:
        return {"error": "Failed to create portfolio."}


def compatible_assets_for_portfolio(portfolio_id: str):
    result = supabase.rpc(
        "get_assets_by_portfolio_base_currency", params={"portfolio_id": portfolio_id}
    ).execute()
    data = result.data
    return result.data if data else None


def check_exchange_assets(exchange_name: str, currency_code: str) -> bool:
    """Check if the specified currency is available on the specified exchange.

    Args:
        exchange_name (str): The name of the exchange in question.
        currency_code (str): The currency code to check.

    Returns:
        bool: Returns True if the currency is available on the exchange, False otherwise.
    """
    result = supabase.rpc(
        "check_exchange_assets",
        {"p_currency_code": currency_code, "p_exchange_name": exchange_name},
    ).execute()
    # Check the result

    if result.data:
        return result.data
    return False


def add_asset_quantity(portfolio_id: str, asset_id: str, quantity: float):
    # Check if the portfolio exists
    portfolio_data = (
        supabase.table("portfolios").select("id").eq("id", portfolio_id).execute()
    )
    if not portfolio_data.data:
        return {"error": f"Portfolio with ID '{portfolio_id}' not found."}

    # Check if the asset exists in the portfolio
    portfolio_asset_data = (
        supabase.table("positions")
        .select("id", "quantity")
        .eq("portfolio_id", portfolio_id)
        .eq("asset_id", asset_id)
        .execute()
    )

    if portfolio_asset_data.data:
        # Asset exists in the portfolio, get the current quantity
        current_quantity = portfolio_asset_data.data[0]["quantity"]
    else:
        # Asset doesn't exist in the portfolio, set the current quantity to 0
        current_quantity = 0
        supabase.table("positions").insert(
            {"portfolio_id": portfolio_id, "asset_id": asset_id, "quantity": quantity}
        ).execute()

    # Calculate the new quantity after addition
    new_quantity = current_quantity + quantity

    # Upsert the asset into the positions table
    update_result = (
        supabase.table("positions")
        .update({"quantity": new_quantity})
        .match({"portfolio_id": portfolio_id, "asset_id": asset_id})
        .execute()
    )

    if update_result.data:
        return {"success": True, "new_quantity": new_quantity}
    else:
        return {"error": "Failed to add or update asset in the portfolio."}


def subtract_asset_quantity(portfolio_id: str, asset_id: str, quantity: float):
    # Check if the portfolio exists
    portfolio_data = (
        supabase.table("portfolios").select("id").eq("id", portfolio_id).execute()
    )
    if not portfolio_data.data:
        return {"error": f"Portfolio with ID '{portfolio_id}' not found."}

    # Check if the asset exists in the portfolio
    portfolio_asset_data = (
        supabase.table("positions")
        .select("id", "quantity")
        .eq("portfolio_id", portfolio_id)
        .eq("asset_id", asset_id)
        .execute()
    )
    if not portfolio_asset_data.data:
        return {"error": f"Asset with ID '{asset_id}' not found in the portfolio."}

    # Get the current quantity of the asset in the portfolio
    current_quantity = portfolio_asset_data.data[0]["quantity"]

    # Calculate the new quantity after subtraction
    new_quantity = max(current_quantity - quantity, 0)

    # Update the quantity in the positions table
    update_result = (
        supabase.table("positions")
        .update({"quantity": new_quantity})
        .match({"portfolio_id": portfolio_id, "asset_id": asset_id})
        .execute()
        # .eq("portfolio_id", portfolio_id)
        # .eq("asset_id", asset_id)
    )

    if update_result.data:
        return {"success": True, "new_quantity": new_quantity}
    else:
        return {"error": "Failed to subtract quantity from the asset in the portfolio."}


def add_generated_prices(asset_id: str):
    """Generate prices for an asset and add them to the database.

    Args:
        asset_id (str): The asset ID to add prices for.

    Raises:
        Exception: Raises an exception if the prices could not be added to the database.

    Returns:
        list[dict]: List of records added to the database.
    """

    price_generator = PriceGenerator(
        num_samples=200, start_time=pendulum.now("utc").subtract(years=3)
    )
    prices_frame = price_generator.generate_df()
    prices_frame["asset_id"] = asset_id
    prices_frame.reset_index(drop=True, inplace=True)
    records = prices_frame.to_dict(orient="records")

    result = supabase.table("asset_prices").insert(records).execute()
    if not result.data:
        raise Exception("Failed to add prices to the database.")
    return result.data if result.data else None
    # repo.add_batch_prices(records)


def sample_compatible_assets(portfolio_id: str, size: int = 5) -> list[dict]:
    compatible = compatible_assets_for_portfolio(portfolio_id)
    if compatible:
        return random.sample(compatible, size)


def generate_prices_for_assets(assets: list[dict]):
    for asset in assets:
        asset_id = asset.get("asset_id")
        added_prices = add_generated_prices(asset_id)
        logger.info(len(added_prices))


def add_random_asset_quantity(portfolio_id: str, asset_id: str):
    random_quantity = random.uniform(0.1, 100)
    add_asset_quantity(portfolio_id, asset_id, random_quantity)


def add_assets_to_portfolio_random_quantity(portfolio_id: str, assets: list[dict]):
    for asset in assets:
        asset_id = asset.get("asset_id")
        add_random_asset_quantity(portfolio_id, asset_id)


def get_portfolio(portfolio_id: str):
    return (
        supabase.rpc("get_portfolio_with_assets", {"p_portfolio_id": portfolio_id})
        .execute()
        .data
    )


def get_closest_asset_price(asset_id: str, timestamp: datetime):
    timestamp = pendulum.instance(timestamp)

    result = supabase.rpc(
        "get_closest_asset_price",
        {"p_asset_id": asset_id, "p_timestamp": timestamp.to_iso8601_string()},
    ).execute()

    if result.data:
        return {
            "asset_id": asset_id,
            "timestamp": timestamp,
            "price": result.data,
        }
    else:
        return {"asset_id": asset_id, "timestamp": timestamp, "price": None}


def get_closest_asset_prices(asset_ids: list[str], timestamp: datetime) -> list[dict]:
    result = supabase.rpc(
        "get_closest_asset_prices",
        {
            "p_asset_ids": asset_ids,
            "p_timestamp": timestamp.isoformat(),
        },
    ).execute()

    if result.data:
        # print(result.data)
        return result.data
    else:
        return []


def get_total_value(portfolio: list[dict]) -> float:
    total_value = 0
    for position in portfolio:
        total_value += position["asset_amount"] * position["asset_value"]
    return total_value


def update_balance(portfolio_id: str, balance: float | None = None):
    portfolio = get_portfolio(portfolio_id)
    balance = balance or get_total_value(portfolio)
    supabase.table("portfolios").update({"balance": balance}).eq(
        "id", portfolio_id
    ).execute()
    # balance = get_total_value(portfolio)


def main():
    # check_exchange_assets("Coinbase Pro", "USDT")
    user_id = select_user_id()
    created_portfolio = create_portfolio(user_id, "USD", "Coinbase Pro")
    portfolio_id = created_portfolio["portfolio_id"]
    compatible_assets = sample_compatible_assets(portfolio_id=portfolio_id, size=3)
    logger.info("Generating prices for the assets")
    generate_prices_for_assets(compatible_assets)

    logger.info("Adding assets to the portfolio")
    add_assets_to_portfolio_random_quantity(portfolio_id, compatible_assets)

    # Get the portfolio and the assets within it.
    devtools.debug(compatible_assets)

    portfolio = get_portfolio(portfolio_id)
    devtools.debug(portfolio)

    closest_price = get_closest_asset_price(
        portfolio[0]["asset_id"], datetime(2023, 1, 1)
    )
    print(closest_price)
    closest_price = get_closest_asset_price(portfolio[0]["asset_id"], datetime.now())
    print(closest_price)
    asset_ids = [asset["asset_id"] for asset in portfolio]
    closest_prices = get_closest_asset_prices(asset_ids, datetime(2023, 1, 1))
    # print(closest_prices)
    update_balance(portfolio_id)
    # Update balance with value * quantity for each position
    # Get all positions for the portfolio
    # get_total_value for each position
    # Update the portfolio balance by getting the sum of all total positions
    # This can be done in a single query using the get_portfolio_with_total_value stored procedure
    # The balance can be updated in the portfolios table
    # IRL I could do a chron jon to update portfolio balances every 15 mins or so.
    # Cron job would increment the value on a table cause a trigger that would update the portfolio balance for each portfolio with a position in the positions table.


if __name__ == "__main__":
    main()
