from __future__ import annotations

from collections.abc import Mapping
from datetime import timedelta
from pathlib import Path
from typing import Any, cast

import atoti as tt
import pandas as pd

from .config import Config
from .constants import StationDetailsTableColumn, StationStatusTableColumn, Table

def read_ue_unit()

def read_station_details(
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
    velib_data_base_path: HttpUrl | Path,
) -> pd.DataFrame:
    stations_data: Any = cast(
        Any,
        read_json(
            velib_data_base_path, Path("station_information.json"), timeout=timeout
        ),
    )["data"]["stations"]
    station_information_df = pd.DataFrame(stations_data)[
        ["station_id", "name", "capacity", "lat", "lon"]
    ].rename(
        columns={
            "station_id": StationDetailsTableColumn.ID.value,
            "name": StationDetailsTableColumn.NAME.value,
            "capacity": StationDetailsTableColumn.CAPACITY.value,
            "lat": "latitude",
            "lon": "longitude",
        }
    )

    # Drop some precision to ensure stability of reverse geocoding results.
    station_information_df = station_information_df.round(
        {"latitude": 6, "longitude": 6}
    )

    coordinates = cast(
        list[tuple[float, float]],
        station_information_df[["latitude", "longitude"]].itertuples(
            index=False, name=None
        ),
    )

    reverse_geocoded_df = reverse_geocode(
        coordinates, reverse_geocoding_path=reverse_geocoding_path, timeout=timeout
    ).rename(
        columns={
            "department": StationDetailsTableColumn.DEPARTMENT.value,
            "city": StationDetailsTableColumn.CITY.value,
            "postcode": StationDetailsTableColumn.POSTCODE.value,
            "street": StationDetailsTableColumn.STREET.value,
            "house_number": StationDetailsTableColumn.HOUSE_NUMBER.value,
        }
    )

    return station_information_df.merge(
        reverse_geocoded_df, how="left", on=["latitude", "longitude"]
    ).drop(columns=["latitude", "longitude"])


def read_station_status(
    velib_data_base_path: HttpUrl | Path,
    /,
    *,
    timeout: timedelta,
) -> pd.DataFrame:
    stations_data = cast(
        Any,
        read_json(velib_data_base_path, Path("station_status.json"), timeout=timeout),
    )["data"]["stations"]
    station_statuses: list[Mapping[str, Any]] = []
    for station_status in stations_data:
        for num_bikes_available_types in station_status["num_bikes_available_types"]:
            if len(num_bikes_available_types) != 1:
                raise ValueError(
                    f"Expected a single bike type but found: {list(num_bikes_available_types.keys())}"
                )
            bike_type, bikes = next(iter(num_bikes_available_types.items()))
            station_statuses.append(
                {
                    StationStatusTableColumn.STATION_ID.value: station_status[
                        "station_id"
                    ],
                    StationStatusTableColumn.BIKE_TYPE.value: bike_type,
                    StationStatusTableColumn.BIKES.value: bikes,
                }
            )
    return pd.DataFrame(station_statuses)


def load_tables(session: tt.Session, /, *, config: Config) -> None:
    station_details_df = read_station_details(
        reverse_geocoding_path=config.reverse_geocoding_path,
        timeout=config.requests_timeout,
        velib_data_base_path=config.velib_data_base_path,
    )
    station_status_df = read_station_status(
        config.velib_data_base_path,
        timeout=config.requests_timeout,
    )

    with session.start_transaction():
        session.tables[Table.STATION_DETAILS.value].load_pandas(station_details_df)
        session.tables[Table.STATION_STATUS.value].load_pandas(station_status_df)
