import asyncio
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
from typing import Set

import devtools
import pendulum as pdm
from decorator import decorator
from loguru import logger
from pydantic import Field, PrivateAttr, computed_field, model_validator
from rich import print
from supamodel._abc import Handler, IgnoreModel
from supamodel._client import client as supabase

# from supamodel.config import supabase_async
from supamodel.enums import RunState, SystemState
from supamodel.trading.clock import Sizing
from supamodel.trading.tokens import AssetData, BaseModel
from supamodel.utils import expose_dual_runtimes


class BacktestRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    window_size: Sizing
    step_size: Sizing


@expose_dual_runtimes
async def async_call():
    await asyncio.sleep(3)
    print("Hello World")


@decorator
def cycle_state(func, *args, **kwargs):
    self: "ClockHandler" = args[0]
    self.load_config()
    result = func(*args, **kwargs)
    self.update_backtest()
    return result


class ClockConfigManager(IgnoreModel):
    """
    A class that manages clock configurations for backtests.
    """

    def by_id(self, id: str, id_type: str = "backtest_id") -> dict:
        """
        Retrieves a clock configuration by its ID.

        Args:
            id (str): The ID of the clock configuration.
            id_type (str, optional): The type of ID to search for. Defaults to "backtest_id".

        Returns:
            dict: The clock configuration data.
        """
        results = (
            supabase.table("backtest_config")
            .select("*")
            .eq(id_type, id)
            .limit(1)
            .execute()
        )
        return results.data[0] if results.data else {}

    def by_config_id(self, config_id: str) -> dict:
        """
        Retrieves a clock configuration by its config ID.

        Args:
            config_id (str): The config ID of the clock configuration.

        Returns:
            dict: The clock configuration data.
        """
        return self.by_id(config_id, "config_id")

    def by_backtest_id(self, backtest_id: str) -> dict:
        """
        Retrieves a clock configuration by its backtest ID.

        Args:
            backtest_id (str): The backtest ID of the clock configuration.

        Returns:
            dict: The clock configuration data.
        """
        return self.by_id(backtest_id, "backtest_id")

    def most_recent(self) -> dict:
        """
        Retrieves the most recent clock configuration.

        Returns:
            dict: The most recent clock configuration data.
        """
        results = (
            supabase.table("backtest_config")
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return results.data[0] if results.data else {}


class ClockHandler(Handler):
    """
    A class that represents a clock handler.

    Attributes:
        window_size (Sizing): The size of the window.
        step_size (Sizing): The size of the step.
        start_time (pdm.DateTime): The start time.
        end_time (pdm.DateTime): The end time.
        backtest_id (str, optional): The backtest ID. Defaults to a new UUID.
        config_id (str, optional): The config ID. Defaults to a new UUID.
        current (pdm.DateTime): The current time.
        _current_time (pdm.DateTime): The current time (private).
        _tail (pdm.DateTime): The tail time (private).
        is_live (bool): Indicates if the clock is live.
        _conf_manager (ClockConfigManager): The clock configuration manager (private).
    """

    # Rest of the code...
    window_size: Sizing = Field(Sizing(weeks=2), repr=False)
    step_size: Sizing = Field(Sizing(days=2), repr=False)
    start_time: pdm.DateTime = pdm.now("UTC")
    end_time: pdm.DateTime = pdm.now("UTC")

    backtest_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()))
    config_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current: pdm.DateTime = pdm.now("UTC")

    _current_time: pdm.DateTime = PrivateAttr(pdm.now("UTC"))
    _tail: pdm.DateTime = PrivateAttr(pdm.now("UTC"))
    is_live: bool = False

    _conf_manager: ClockConfigManager = PrivateAttr(ClockConfigManager())

    @model_validator(mode="after")
    def validate_time(self) -> None:
        self.load_config()
        if self.start_time < self.current:
            self.current = self.start_time

    def required(self) -> Set[str]:
        return set(["config_id"])

    @computed_field
    @property
    def head(self) -> pdm.DateTime:
        if self.is_live:
            return pdm.now("UTC")
        return self.current

    @computed_field
    @property
    def tail(self) -> pdm.DateTime:
        return self.head.subtract(**self.window_size_dump)

    @property
    def window_size_dump(self, is_json: bool = False) -> dict:
        mode = "json" if is_json else "python"
        return self.window_size.model_dump(mode=mode, round_trip=True)

    @property
    def step_size_dump(self, is_json: bool = False) -> dict:
        mode = "json" if is_json else "python"
        return self.step_size.model_dump(mode=mode, round_trip=True)

    @cycle_state
    def reset(self, options={}, *args, **kwargs) -> None:
        if self.is_live:
            return None
        if self.start_time < self.current:
            self.current = self.start_time

    @cycle_state
    def step(self) -> None:
        if self.is_live:
            return None
        self.current = self.current.add(**self.step_size_dump)

    def is_finished(self) -> bool:
        return self.current >= self.end_time and not self.is_live

    def change_window(self, window_size: Sizing) -> None:
        self.window_size = window_size
        supabase.table("backtest_config").update(
            {"window_size": self.window_size_dump}
        ).eq("backtest_id", self.backtest_id).execute()

    def change_stepsize(self, step_size: Sizing) -> None:
        self.step_size = step_size
        supabase.table("backtest_config").update({"step_size": self.step_size_dump}).eq(
            "backtest_id", self.backtest_id
        ).execute()

    # ___________________________________________
    #  Database Operations
    # ___________________________________________

    def complex_update(self) -> dict:
        supabase.table("backtest_config").update(self.get_config()).eq(
            "config_id", self.config_id
        ).execute()

    def update_config(self) -> dict:
        config = self.get_config()
        config["config_id"] = self.config_id or str(uuid.uuid4())
        updated = supabase.table("backtest_config").upsert(config).execute()
        return updated.data[0] if updated.data else {}
        # devtools.debug(updated)

    def get_config(self) -> dict:
        return {
            "window_size": self.window_size.model_dump(mode="json", round_trip=True),
            "step_size": self.step_size.model_dump(
                round_trip=True,
                mode="json",
            ),
            "current": self.current.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "backtest_id": self.backtest_id,
            "config_id": self.config_id,
            "created_at": pdm.now("UTC").isoformat(),
        }

    @expose_dual_runtimes
    def load_config(self) -> dict:
        config = (
            supabase.table("backtest_config")
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        current_config = config.data[0] if config.data else {}

        if not current_config:
            return {}
        self.set_conf_vars(current_config)

        return config

    def load_recent_config(self) -> dict:
        config = (
            supabase.table("backtest_config")
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        current_config = config.data[0] if config.data else {}
        logger.debug(current_config)
        if not current_config:
            return {}
        self.set_conf_vars(current_config)

        return config

    def set_conf_vars(self, current_config):
        self.window_size = Sizing(**current_config["window_size"])
        self.step_size = Sizing(**current_config["step_size"])
        self.current = pdm.parse(current_config["current"])
        self.start_time = pdm.parse(current_config["start_time"])
        self.end_time = pdm.parse(current_config["end_time"])
        self.backtest_id = current_config["backtest_id"]
        self.config_id = current_config["config_id"]
        self.is_live = current_config.get("is_live", False)

    def load_by_config_id(self, config_id: str) -> dict:
        current_config = self._conf_manager.by_config_id(config_id)
        if not current_config:
            return {}
        self.set_conf_vars(current_config)

        return current_config

    def load_by_backtest(self, backtest_id: str) -> dict:
        current_config = self._conf_manager.by_backtest_id(backtest_id)
        if not current_config:
            return {}
        return self.set_conf_vars(current_config)

    def update_backtest(self) -> dict:
        # config = self.get_config()
        updated = (
            supabase.table("backtest_config")
            .update({"current": self.current.isoformat(), "is_live": self.is_live})
            .eq("backtest_id", self.backtest_id)
            .execute()
        )
        return updated.data[0] if updated.data else {}

    def load_config(self) -> dict:  # noqa: F811
        # Load by config_id
        config = {}
        if not config:
            config = self.load_by_backtest(self.backtest_id)

            if config:
                return config

        if self.config_id:
            config = self.load_by_config_id(self.config_id)
            if config:
                return config
        # if not config:
        #     config = self.load_recent_config()
        if not config:
            config = self.update_config()

        self.load_recent_config()

    def most_recent_config(self) -> pdm.DateTime:

        return pdm.now("UTC")


class DataHandler(Handler):
    # run_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()))
    # run_state: RunState = RunState.PENDING
    # system_state: SystemState = SystemState.BACKTEST
    backtest_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()))
    # config_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def clock(self) -> "ClockHandler":
        handle = ClockHandler(backtest_id=self.backtest_id)
        handle.load_config()
        return handle

    @abstractmethod
    def closest(self, timestamp: datetime | None = None, *args, **kwargs):
        """Gets the closest data point to the current time. Before or equal to the current time."""
        pass

    @abstractmethod
    def latest(self, *args, **kwargs):
        """Gets the latest data point."""
        pass

    @abstractmethod
    def between(self, *args, **kwargs):
        """Gets data points between two times."""
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        """Gets all data points."""
        pass

    @abstractmethod
    def by_range(self, *args, **kwargs):
        """Gets data points by a given range."""
        pass

    @abstractmethod
    def by_field(self, *args, **kwargs):
        """Gets data points by a given field."""
        pass


async def main():
    backtest_request = BacktestRequest(
        start_time=pdm.now("UTC").subtract(years=2),
        end_time=pdm.now("UTC"),
        window_size=Sizing(weeks=1),
        step_size=Sizing(days=1),
    )
    clock = ClockHandler(
        backtest_id="723cb164-865c-4b1a-9a20-5f5eb09e8b28",
        window_size=backtest_request.window_size,
        step_size=backtest_request.step_size,
        start_time=backtest_request.start_time,
        end_time=backtest_request.end_time,
    )

    clock.reset()
    clock.is_live = False
    # devtools.debug(clock)
    while not clock.is_finished():
        # for _ in range(20):
        clock.step()
        devtools.debug(clock)
    # print(clock)
    # clock.reset()
    # clock.step()
    # devtools.debug(clock)

    # await clock.save_config_async()
    # print(clock)


if __name__ == "__main__":
    asyncio.run(main())
