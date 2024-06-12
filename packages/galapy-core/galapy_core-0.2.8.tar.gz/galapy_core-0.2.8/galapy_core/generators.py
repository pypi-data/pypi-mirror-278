import random
import uuid
from typing import List

import pendulum as pdm
from supamodel.enums import TimeIntSQL
from supamodel.trading.market_data import Price, PriceBar


def now_utc():
    return pdm.now("UTC")


def create_price_bars(num_bars: int) -> List[PriceBar]:

    price_bars = []

    for _ in range(num_bars):
        price_bar = PriceBar(
            address=uuid.uuid4().hex,
            interval=random.choice(["1m", "5m", "15m", "30m", "1h", "4h", "1d"]),
            close=random.uniform(0, 1000),
            high=random.uniform(0, 1000),
            low=random.uniform(0, 1000),
            open=random.uniform(0, 1000),
            volume=int(random.uniform(0, 1000000)),
            timestamp=now_utc().subtract(days=random.randint(1, 300)),
        )
        price_bars.append(price_bar)

    return price_bars


def create_prices(num_prices: int) -> List[Price]:
    prices = []
    for _ in range(num_prices):
        price = Price(
            **{
                "address": uuid.uuid4().hex,
                "price": random.uniform(0, 1000),
                "timestamp": now_utc().subtract(days=random.randint(1, 300)),
            }
        )
        prices.append(price)
    return prices
