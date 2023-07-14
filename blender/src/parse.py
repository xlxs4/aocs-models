import csv
from datetime import datetime
from pathlib import Path
from typing import Any, List

from config import config
from eltypes import CSVRow, Data, DatumParser, Quaternion, Time


def parse_csv(
    filename: Path,
    parse_datum: DatumParser,
    remove_header: bool = True,
    **kwargs: Any
) -> List:
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        if remove_header:
            next(reader)
        return [parse_datum(row, **kwargs) for row in reader]


def _parse_quaternion(row: CSVRow) -> Quaternion:
    return Quaternion(
        float(row['q4']), float(row['q1']), float(row['q2']), float(row['q3'])
    )


def _parse_time(row: CSVRow) -> Time:
    return Time(
        datetime.strptime(row['Time (UTCG)'], "%d %b %Y %H:%M:%S.%f"),
        scale='utc'
    )


def _parse_float(row: CSVRow, column: str) -> float:
    return float(row[column])


def parse_data() -> Data:
    times = parse_csv(config.paths.stk_quaternion, _parse_time)
    quaternions = parse_csv(config.paths.stk_quaternion, _parse_quaternion)
    areas = parse_csv(
        config.paths.stk_area, _parse_float, column='Effective Area (m^2)'
    )
    powers = parse_csv(config.paths.stk_power, _parse_float, column='Power (W)')

    return times, quaternions, areas, powers
