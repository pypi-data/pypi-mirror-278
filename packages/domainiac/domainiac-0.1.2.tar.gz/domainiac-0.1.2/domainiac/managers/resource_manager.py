import datamazing.pandas as pdz
import pandas as pd
from typeguard import typechecked


class ResourceManager:
    """
    Manager which simplifies the process of handling resource schedules.
    """

    def __init__(
        self,
        db: pdz.Database,
        time_interval: pdz.TimeInterval,
    ) -> None:
        self.db = db
        self.time_interval = time_interval

    @typechecked
    def get_resource_schedules(
        self,
        resource_gsrns: list,
    ) -> pd.DataFrame:
        """Gets resource schedules for a given list of resource gsrns."""
        df_resource_schedules = self.db.query(
            table_name="resourceSchedule",
            time_interval=self.time_interval,
            filters={"resource_gsrn": resource_gsrns},
        )
        df_resource_schedules = df_resource_schedules.filter(
            [
                "market_participant",
                "created_time_utc",
                "price_area",
                "resource_gsrn",
                "main_fuel_type",
                "is_sum_plan",
                "time_utc",
                "schedule_power_MW",
                "schedule_capacity_min_MW",
                "schedule_capacity_max_MW",
            ]
        )
        return df_resource_schedules

    @typechecked
    def get_latest_resource_plan(
        self,
        resource_gsrns: list,
    ) -> pd.DataFrame:
        """Gets the lastest resource schedules for a given list of resource gsrns."""

        df_resource_schedules = self.get_resource_schedules(
            resource_gsrns=resource_gsrns
        )

        df_latest_created_time = pdz.group(
            df=df_resource_schedules, by=["resource_gsrn", "time_utc"]
        ).agg({"created_time_utc": max})

        df_resource_latest = df_latest_created_time.merge(
            df_resource_schedules, on=list(df_latest_created_time.columns)
        )

        return df_resource_latest
