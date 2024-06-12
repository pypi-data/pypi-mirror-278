import datamazing.pandas as pdz
import pandas as pd

from .masterdata_manager import MasterdataManager


class PlantManager(MasterdataManager):
    """
    Manager which simplifies the process of getting plants from masterdata.
    """

    def __init__(
        self,
        db: pdz.Database,
        time_interval: pdz.TimeInterval,
        resolution: pd.Timedelta,
    ) -> None:
        self.db = db
        self.time_interval = time_interval
        self.resolution = resolution

    def get_plants(
        self,
        filters: dict = {},
        columns: list = [
            "plant_id",
            "masterdata_gsrn",
            "datahub_gsrn_e18",
            "installed_power_MW",
            "price_area",
            "is_tso_connected",
            "valid_from_date_utc",
            "valid_to_date_utc",
        ],
    ) -> pd.DataFrame:
        """Gets the plants for a given plant type.
        Filters for plants valid at the end of time interval.
        Filters by default for plants in operation.
        """
        return self.get_data("masterdataPlant", filters=filters, columns=columns)

    def get_installed_power_timeseries(self, gsrn: str) -> pd.DataFrame:
        """Gets the installed power timeseries for a plant."""

        df_times = self.time_interval.to_range(self.resolution).to_frame(
            index=False, name="time_utc"
        )

        # explode plant to time series
        df_plant = self.get_operational_entities("masterdataPlant")
        df_plant = df_plant.query(f"masterdata_gsrn == '{gsrn}'")

        df_plant = pdz.merge(
            df_times,
            df_plant,
            left_time="time_utc",
            right_period=("valid_from_date_utc", "valid_to_date_utc"),
        )

        return df_plant.filter(["time_utc", "installed_power_MW"]).reset_index(
            drop=True
        )
