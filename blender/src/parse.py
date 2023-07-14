import csv
from typing import Callable, Dict, List, Tuple, Any
from pyquaternion import Quaternion
from astropy.time import Time
from datetime import datetime
from pathlib import Path
from here import here
from config import config


def parse_csv(
    filename: Path,
    data_type: Callable[[Dict[str, str]], Any],
    remove_header: bool = True,
    **kwargs: Any
) -> List[Any]:
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        if remove_header:
            next(reader)
        return [data_type(row, **kwargs) for row in reader]


def _parse_quaternion(row: Dict[str, str]) -> Quaternion:
    return Quaternion(
        float(row['q4']), float(row['q1']), float(row['q2']), float(row['q3'])
    )


def _parse_time(row: Dict[str, str]) -> Time:
    return Time(
        datetime.strptime(row['Time (UTCG)'], "%d %b %Y %H:%M:%S.%f"),
        scale='utc'
    )


def _parse_float(row: Dict[str, str], column: str) -> float:
    return float(row[column])


def parse_data(
) -> Tuple[List[Time], List[Quaternion], List[float], List[float]]:
    times = parse_csv(config.paths.stk_quaternion, _parse_time)
    quaternions = parse_csv(config.paths.stk_quaternion, _parse_quaternion)
    areas = parse_csv(
        config.paths.stk_area, _parse_float, column='Effective Area (m^2)'
    )
    powers = parse_csv(config.paths.stk_power, _parse_float, column='Power (W)')

    return times, quaternions, areas, powers
