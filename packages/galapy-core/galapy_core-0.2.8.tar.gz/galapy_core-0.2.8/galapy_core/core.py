from supamodel._abc import BaseModel

from galapy_core.assets import AssetClient
from galapy_core.market_data import MarketDataClient
from galapy_core.metrics import MetricClient
from galapy_core.portfolio import PortfolioClient


class GalaxyBackroom(BaseModel):
    @property
    def assets(self):
        return AssetClient()

    @property
    def market_data(self) -> MarketDataClient:
        return MarketDataClient()

    @property
    def metrics(self) -> "MetricClient":
        return MetricClient()

    @property
    def portfolio(self) -> PortfolioClient:
        return PortfolioClient()

    @property
    def account(self):
        pass

    @property
    def order(self):
        pass

    @property
    def trade(self):
        pass

    @property
    def wallet(self):
        pass

    @property
    def defi(self):
        pass


def main():
    backroom = GalaxyBackroom()
    # backroom.assets.add_asset()


if __name__ == "__main__":
    main()
