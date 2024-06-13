import datamazing.pandas as pdz
import pandas as pd
from typeguard import typechecked


class MasterdataManager:
    """
    Manager which simplifies the process of getting units from masterdata.
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

    @typechecked
    def get_operational_entities(self, table: str, filters: dict = {}) -> pd.DataFrame:
        """Gets the operational data for a given table."""

        filters["standing_entity_state"] = "InOperation"
        df = self.db.query(table, filters=filters)
        return df

    @typechecked
    def get_data(
        self, table: str, filters: dict = {}, columns: list = []
    ) -> pd.DataFrame:
        """Gets the data for a given table.
        Filters for rows valid at the end of time interval.
        """
        df = self.get_operational_entities(table, filters)

        for column in columns:
            if column not in df.columns:
                raise KeyError(f"Column {column} not found in {table}")

        df = pdz.as_of_time(
            df=df,
            period=("valid_from_date_utc", "valid_to_date_utc"),
            at=self.time_interval.right,
        )
        df = df.filter(columns)

        return df
