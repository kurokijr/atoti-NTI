from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import IO

import pandas as pd
import requests
from pydantic import HttpUrl

_Coordinates = tuple[float, float]  # (latitude, longitude)


@lru_cache
def _cached_reverse_geocode(
    stable_coordinates: tuple[_Coordinates, ...],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
) -> pd.DataFrame:
    data: StringIO | Path

    if isinstance(reverse_geocoding_path, HttpUrl):
        file = StringIO()
        pd.DataFrame(stable_coordinates, columns=["latitude", "longitude"]).to_csv(
            file, index=False
        )
        file.seek(0)
        _file: IO[str] = file  # To make Mypy happy.
        response = requests.post(
            reverse_geocoding_path,
            files={"data": _file},
            timeout=timeout.total_seconds(),
        )
        response.raise_for_status()
        data = StringIO(response.text)
    else:
        # mypy fails to refines the type of `reverse_geocoding_path` to `Path`.
        data = reverse_geocoding_path  # type: ignore[assignment]

    results_df = pd.read_csv(data)
    results_df = results_df.rename(
        columns={
            "result_context": "department",
            "result_city": "city",
            "result_postcode": "postcode",
            "result_name": "street",
            "result_housenumber": "house_number",
        }
    )
    results_df = results_df[
        [
            "latitude",
            "longitude",
            "department",
            "city",
            "postcode",
            "street",
            "house_number",
        ]
    ]
    return results_df


def reverse_geocode(
    data: Iterable[_Coordinates],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
) -> pd.DataFrame:
    return _cached_reverse_geocode(
        tuple(sorted(data)),
        reverse_geocoding_path=reverse_geocoding_path,
        timeout=timeout,
    )
