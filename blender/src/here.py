from pathlib import Path
from typing import Union


class SUSoftwareError(Exception):
    """Base error class for SU Software"""


class ProjectIndicatorNotFound(SUSoftwareError):
    """The project indicator file (e.g. `.here`) was not found in this or any parent directory"""


def find_root(
    path: Union[str, Path] = Path.cwd(), project_indicator: str = ".here"
) -> Path:
    """
    Find the root directory for the project based on the presence of a project indicator file.

    :param path: The path to start searching from. Default is the current working directory.
    :param project_indicator: The file name used to indicate the project root.
    :return: The project root directory.
    """
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


def here(*paths: Union[str, Path], as_str: bool = False) -> Path:
    """
    Resolve the absolute path for the given relative path components within the project root.

    :param paths: The relative path components.
    :return: The absolute path.
    """
    root = find_root()
    res = root.joinpath(*paths).resolve()
    return str(res) if as_str else res
