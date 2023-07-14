from typing import Any, Callable, Dict, List, Tuple

from astropy.time import Time as _Time
from pyquaternion import Quaternion as _Quaternion
from skyfield.jpllib import SpiceKernel as _SpiceKernel
from skyfield.positionlib import ICRF as _ICRF

Time = _Time
Quaternion = _Quaternion
SpiceKernel = _SpiceKernel
ICRF = _ICRF
CSVRow = Dict[str, str]
Data = Tuple[List[Time], List[Quaternion], List[float], List[float]]
DatumParser = Callable[[CSVRow], Any]