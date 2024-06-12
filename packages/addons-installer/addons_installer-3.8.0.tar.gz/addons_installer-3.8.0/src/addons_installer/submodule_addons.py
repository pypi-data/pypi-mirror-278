"""
This file contains the submodule addons extract functionality.

The extract function is the entry point to find all the submodules of a given path.
"""
import logging
import pathlib
import subprocess
from typing import List, Tuple, Union

from .api import BaseAddonsResult, OdooAddonsDef

_logger = logging.getLogger("addons_installer:submodule")

__all__ = ["extract"]


def extract(path: pathlib.Path, *, force_include: bool = False) -> List[OdooAddonsDef]:
    """
    Extract the path from the giut submodule of the path.
    Only if the submodule exist on the file disk, can be forced with `force_include=True`
    Args:
        path: The path to lookup
        force_include: Force the submodule even not initialized
    Returns: A list of addons path
    """
    submodules = []
    lines = _extract_submodule_config(path)
    if lines:
        _logger.info("Submodule detected in %s", str(path))
    for line in lines:
        addon_name, addon_path = _parse_git_submodule_result(line, key_to_find="path")
        if not addon_name or not addon_path:
            continue
        addon_full_path = path / addon_path
        if force_include or addon_full_path.exists():
            submodules.append(BaseAddonsResult(addon_name, str(addon_full_path.resolve())))
    return submodules


def _extract_submodule_config(path: pathlib.Path) -> List[str]:
    """
    Extract all the config from the file `.gitmodules` in the path if thius file exist.
    Use `git config` subcommand to do that.
    Args:
        path: The path where `.gitmodules` is located
    Returns: The lines of the .gitmodules file.
    """
    current_sub = path / ".gitmodules"
    if not path.exists() or not current_sub.exists():
        return []
    _logger.info("Submodule detected in %s", str(path))
    output = subprocess.check_output(["git", "config", "--list", f"--file={current_sub}"], text=True)
    return output.splitlines()


def _parse_git_submodule_result(line: str, key_to_find: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Parse a line from a `.gitmodules` config file.
    The line must start with `"submodule"` and end with `key_to_find` to be return
    Otherwise `None` is returned
    Args:
        line: A line from the file
    Returns: The key and the value of the key_to_find
    """
    try:
        key, value = line.split("=")
        key_frag = key.split(".")
        if key_frag[0] != "submodule":
            return None, None
        if key_frag[-1] != key_to_find:
            return None, None
        submodule_name = ".".join(key_frag[1:-1])
        return submodule_name, value
    except ValueError:
        return None
