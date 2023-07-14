from collections import namedtuple
from dataclasses import dataclass
from typing import Union
from pathlib import Path
from here import here


_Paths = namedtuple(
    "Paths", ["blender_model", "stk_quaternion", "stk_area", "stk_power"]
)

@dataclass
class _Config:
    solar_panel_efficiency: float = 0.285
    performance_ratio: float = 1
    max_sun_constant: float = 1413.0
    min_sun_constant: float = 1322.0
    pixels_per_m2: float = 264921.8466012359
    stations_url: str = 'http://celestrak.org/NORAD/elements/stations.txt'
    paths: _Paths = _Paths(
        blender_model=here('model/new_model.blend', as_str=True),
        stk_quaternion=here('stk/quaternion.csv'),
        stk_area=here('stk/area.csv'),
        stk_power=here('stk/power.csv')
    )

config = _Config()
