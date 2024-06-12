import asyncio
import json
import random
import uuid
from datetime import datetime
from typing import List

import pandas as pd
import pendulum
from postgrest._async.request_builder import (
    AsyncFilterRequestBuilder,
    AsyncRequestBuilder,
)
from postgrest._sync.request_builder import SyncRequestBuilder
from postgrest.base_request_builder import BaseFilterRequestBuilder
from rich import print
from supabase.client import PostgrestAPIError
from supamodel._abc import BaseModel
from supamodel._client import client as supabase
from supamodel._core import Metric, TimeData
from supamodel.utils import expose_dual_runtimes

num_entries = 100  # Number of entries to generate
start_date = datetime(2023, 1, 1)  # Start date for timestamps
end_date = datetime(2023, 12, 31)  # End date for timestamps
metric_types = [
    "balance",
    "price",
    "cash",
    "portfolio",
    "service",
    "performance",
]  # Possible metric types


class MetricClient(BaseModel):

    @classmethod
    def table(cls) -> SyncRequestBuilder:
        return supabase.table("metrics")

    def store_one(
        self,
        metric_type: str,
        name: str,
        timestamp: datetime,
        value: float,
        backtest_id: str | None = None,
        metadata: dict = {},
    ):
        if backtest_id:
            metadata["backtest_id"] = backtest_id
        return self.table.insert(
            {
                "type": metric_type,
                "name": name,
                "timestamp": timestamp,
                "value": value,
                "metadata": metadata,
            }
        ).execute()

    def store_batch(
        self,
        metrics: List[dict],
        backtest_id: str | None = None,
        metadata: dict = {},
        metric_time: datetime | None = None,
    ):
        insertable = self.process_metrics_data(
            metrics, backtest_id, metadata, metric_time
        )

        return self.table.insert(insertable).execute()

    def store_many(
        self,
        metric_map: dict,
        backtest_id: str | None = None,
        metrci_time: datetime | None = None,
        metadata: dict = {},
    ):
        if not metric_map:
            raise ValueError("No metrics to insert.")

        metrics_models = [
            Metric(
                type=metric_map.get("type"),
                name=name,
                timestamp=metric_map.get("timestamp"),
                value=value,
                metadata=metric_map.get("metadata"),
            )
            for name, value in metric_map.items()
        ]

        insertable_metrics = list(
            map(
                lambda x: x.model_dump(mode="json", exclude_none=True, by_alias=True),
                metrics_models,
            )
        )

        insertable_metrics = self.process_metrics_data(
            insertable_metrics, backtest_id, metadata, metrci_time
        )

        return self.table.insert(insertable_metrics).execute()

    def get_between(
        self, metric_type: str, name: str, start_time: datetime, end_time: datetime
    ):
        return (
            self.table.select("*")
            .match({"type": metric_type, "name": name})
            .gte("timestamp", start_time)
            .lte("timestamp", end_time)
            .execute()
        )

    def get_all(self):
        return self.table.select("*").execute()

    def process_metrics_data(
        self,
        metrics: List[dict],
        backtest_id: str | None = None,
        metadata: dict = {},
        metric_time: datetime | None = None,
    ) -> List[dict]:
        for metric in metrics:
            current_metric = metric.get("metadata", {})
            if metadata:
                current_metric.update(metadata)
            if backtest_id:
                metric["metadata"]["backtest_id"] = backtest_id
            if metric_time:
                metric["timestamp"] = metric_time
        return metrics


class MetricInput(BaseModel):
    type: str = "metric"
    name: str | None = None
    metadata: dict = {}


def random_timestamp(start, end):
    start = pendulum.instance(start)
    end = pendulum.instance(end)
    return start.add(seconds=random.randint(0, (end - start).in_seconds()))


def random_metadata():
    return {
        "instrument": random.choice(["ABC123", "DEF456", "GHI789"]),
        "exchange": random.choice(["NYSE", "NASDAQ", "CME"]),
        "details": {
            "user": f"user{int(random.gauss(22, 10))}",
            "session": f"session{random.randint(1, 10)}",
            # It could also put in backtest_id, strategy_id, etc. as needed
            "strategy_id": str(uuid.uuid4()),
        },
        "physical": {
            "location": {
                "lon": random.uniform(-180, 180),
                "lat": random.uniform(-90, 90),
            },
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": random.choice(["NY", "CA", "TX", "FL"]),
                "zip": "".join([str(random.randint(0, 9)) for _ in range(5)]),
            },
        },
    }


def generate_metrics(entry_count: int = 100) -> List[dict]:
    # num_entries = 100  # Number of entries to generate
    {
        "name": "feature_name",
        "description": "feature_description",
        "dtype": "feature_type",
        "value": "feature_value",
        "timestamp": "feature_timestamp",
    }
    return [
        Metric(
            **{
                "type": random.choice(metric_types),
                "name": f"metric_{i}",
                "timestamp": random_timestamp(start_date, end_date).isoformat(),
                "value": round(random.uniform(1, 1000), 2),
                "metadata": random_metadata(),
            }
        )
        for i in range(1, entry_count + 1)
    ]


@expose_dual_runtimes
async def insert_metric(metric: Metric) -> Metric:

    response = (
        supabase.table("metrics").insert(metric.supa_dump(by_alias=True)).execute()
    )
    resp_data = response.data
    resp_data if resp_data else []
    if not resp_data:
        raise PostgrestAPIError("Failed to add metric to the database.")
    return resp_data


@expose_dual_runtimes
async def insert_metrics(metrics: List[Metric]) -> List[Metric]:
    list_dict = [metric.supa_dump(by_alias=True) for metric in metrics]
    try:
        response = supabase.table("metrics").insert(list_dict).execute()
        resp_data = response.data
        resp_data if resp_data else []
        if not resp_data:
            raise PostgrestAPIError("Failed to add metrics to the database.")
        return resp_data
    except Exception as e:
        raise e


def get_metrics(metric: MetricInput, time_data: TimeData):
    response = (
        supabase.table("metrics")
        .select("*")
        .eq("type", metric.type)
        .gte("timestamp", time_data.start_time.to_iso8601_string())
        .lte("timestamp", time_data.end_time.to_iso8601_string())
        .order("timestamp", desc=True)
        .execute()
    )

    return response.data if response.data else []


def main():
    metadatas = generate_metrics(entry_count=1000)
    minput = MetricInput(metadata={"exchange": "NYSE"}, type="balance")
    time_data = TimeData(
        start_time=pendulum.instance(start_date),
        end_time=pendulum.instance(end_date),
    )
    insert_metrics(metadatas)
    # print()
    metric_df = pd.DataFrame(get_metrics(minput, time_data))
    metric_df.sort_values("timestamp", ascending=False, inplace=True)
    print(metric_df)

    # For certain calls, we'll be able to insert multiple metrics with the same data by ising the key/value from dicts to determine the name and value of the metric.

    # We can just create a list of dictionaries with the same keys and values as the metrics we want to insert.

    many_metrics_container = {
        "type": "risk",
        "timestamp": pendulum.now().subtract(years=1, months=3, days=2).isoformat(),
        "metrics": {
            "max_drawdown": 10.0,
            "sharpe_ratio": 1.5,
            "sortino_ratio": 1.0,
            "calmar_ratio": 1.0,
            "volatility": 0.1,
            "win_rate": 1,
            "loss_rate": 0,
            "profit_factor": 1.0,
            "average_win": 1.0,
            "average_loss": 0.0,
            "average_trade": 0.0,
            "max_consecutive_wins": 0,
            "max_consecutive_losses": 0,
            "average_holding_period": 0,
            "omega_ratio": 1.0,
        },
        "metadata": {
            "backtest_id": "123",
        },
    }

    metrics_dict = many_metrics_container.get("metrics")

    metrics_models = [
        Metric(
            type=many_metrics_container.get("type"),
            name=name,
            timestamp=many_metrics_container.get("timestamp"),
            value=value,
            metadata=many_metrics_container.get("metadata"),
        )
        for name, value in metrics_dict.items()
    ]

    insertable = list(
        map(
            lambda x: x.model_dump(mode="json", exclude_none=True, by_alias=True),
            metrics_models,
        )
    )
    insert_metrics(metadatas)
    print(insertable)

    metric_df = pd.DataFrame(get_metrics(minput, time_data))
    metric_df.sort_values("timestamp", ascending=False, inplace=True)

    print(metric_df)
    # minput
    # print(pd.DataFrame(metadatas).to_dict())
    # print(json.dumps(metadatas, indent=4))


if __name__ == "__main__":
    main()
