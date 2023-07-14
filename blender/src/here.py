from pathlib import Path
from typing import Union


class SUSoftwareError(Exception):
    """Base error class for SU Software"""


class ProjectIndicatorNotFound(SUSoftwareError):
    """The project indicator file (e.g. `.here`) was not found in this or any parent directory"""


def find_root(
    path: Union[str, Path] = Path.cwd(), project_indicator: str = ".here"
) -> Path:
    path = Path(path).resolve()

    while path.parent != path:
        if path.joinpath(project_indicator).exists():
            return path
        path = path.parent

    if path.joinpath(project_indicator).exists():
        return path

    raise ProjectIndicatorNotFound(
        f"The project indicator file '{project_indicator}' was not found in this or any parent directory of {str(path)}"
    )


def here(*paths: Union[str, Path], as_str: bool = False) -> Union[str, Path]:
    root = find_root()
    res = root.joinpath(*paths).resolve()
    return str(res) if as_str else res
