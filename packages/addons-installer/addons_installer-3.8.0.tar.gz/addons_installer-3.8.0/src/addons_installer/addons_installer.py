import logging
import pathlib
import shutil
import subprocess
import sys
import warnings
from os.path import exists as path_exists
from os.path import join as path_join
from typing import Dict, List, Set, Type, Union

from . import submodule_addons
from .api import AddonsSuffix, OdooAddonsDef
from .git_addons import GitOdooAddons, GitSubDirOdooAddons, LegacyDepotGit
from .local_addons import LocalOdooAddons, LocalSubDirOdooAddons

_logger = logging.getLogger("install_addons")
_logger.setLevel(logging.INFO)

PIP_EXEC = shutil.which("pip")
NPM_EXEC = shutil.which("npm")


class AddonsFinder(object):
    """
    This class try o find all the Odoo dependency Addons from Environ Var
    The Odoo Addons can be declared in 2 ways.
    ADDONS_GIT_XXX or ADDONS_LOCAL_XXX
    In case of `ADDONS_GIT_XXX` then [GitOdooAddons][GitOdooAddons] is used to discover all other necessary Key
    In case of `ADDONS_LOCAL_XXX` then [LocalODooAddons][LocalODooAddons] is used.
    All supported types are defined in `types`

    Attributes:
        type: Contains all the supported Addons Type
    """

    types: List[Type[AddonsSuffix]] = [
        GitSubDirOdooAddons,
        LocalSubDirOdooAddons,
        GitOdooAddons,
        LocalOdooAddons,
        LegacyDepotGit,
    ]

    @staticmethod
    def get_addons(env_vars: Dict[str, str] = None) -> Set[AddonsSuffix]:
        founded = {}
        for env_key in sorted(env_vars.keys()):
            addon = AddonsFinder.try_parse_key(env_key)
            if addon and env_vars.get(env_key) != str(False):
                _logger.info(f"Found depends {addon} from {addon.identifier}")
                founded[addon.identifier] = addon
        return set(founded.values())

    @staticmethod
    def _include_odoo_path(env_vars: Dict[str, str]) -> Dict[str, str]:
        """
        If `ODOO_PATH` is in `env_vars` then we add the native odoo addons path in env.
        With this function we handle the native Odoo addons like any other addons
        :param env_vars: the current env to parse
        :return: a copy of the env with ADDONS_LOCAL
        """
        result = dict(env_vars)
        if result.get("ODOO_PATH"):
            # In the new Docker image, we have a /odoo where odoo is cloned
            # inside /odoo/ooo and /odoo contains the conf file too
            odoo_path = path_join(result.get("ODOO_PATH"), "odoo")
            if "ADDONS_LOCAL_SRC_ODOO_ADDONS" not in env_vars:
                result["ADDONS_LOCAL_SRC_ODOO_ADDONS"] = path_join(odoo_path, "odoo", "addons")
            if "ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS" not in env_vars:
                result["ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS"] = path_join(odoo_path, "addons")
        return result

    @staticmethod
    def parse_env(env_vars: Dict[str, str] = None) -> Set[OdooAddonsDef]:
        """
        Parse the provided environment dict to find addons in it.
        The submodule addons are not find, only GitAddons, LegacyAddons, and LocalAddons or founded
        See Also `parse_submodule` to find the submodule of each addon path.

        Args:
            env_vars: The dict containing the variable to lookup

        Returns: The set of Addons founded. The addons not necessary exist on disc. See GitAddons.

        """
        env_vars = AddonsFinder._include_odoo_path(env_vars)
        return {f.extract(env_vars) for f in AddonsFinder.get_addons(env_vars)}

    @staticmethod
    def parse_submodule(addons: List[OdooAddonsDef], *, include_not_exist=False) -> List[OdooAddonsDef]:
        """
        find in each addons a `.gitmodule` file.
        If one is found, then we parse the file and add the submodule to the result.
        The submodule is added to the result only if his path exist,
        this behavior can be forced with `include_not_exist=True`

        Args:
            addons: A list of add-ons path to lookup in
            include_not_exist: Force submodule to be in the result even if his path don't exist

        Returns: A list with the new add-ons path found
        """
        addons_def: List[OdooAddonsDef] = []
        for result in addons:
            addons_def.extend(
                submodule_addons.extract(pathlib.Path(result.addons_path), force_include=include_not_exist)
            )
        return addons_def

    @staticmethod
    def try_parse_key(env_key: str) -> Union[AddonsSuffix, None]:
        """

        :param env_key:
        :return:
        """
        for addon_type in AddonsFinder.types:
            addons: AddonsSuffix = addon_type(env_key)
            if addons.is_valid():
                return addons
        return None


class AddonsRegistry(AddonsFinder):
    """
    Compatibility with 1.5.0
    @see AddonsFinder
    """

    def __init__(self):
        warnings.warn("Deprecated, use AddonsFinder insted. will be removed in 2.0.0", DeprecationWarning)
        super(AddonsRegistry, self).__init__()


class OdooAddonsDefInstaller(OdooAddonsDef):
    def install(self):
        AddonsInstaller.install(self)


class AddonsInstaller:
    @staticmethod
    def exec_cmd(cmd: List[str], force_log=True, cwd: str = None) -> int:
        if not cmd:
            return 0
        if force_log:
            _logger.info(">> %s", " ".join(cmd))
        return AddonsInstaller.exit_if_error(subprocess.Popen(cmd, cwd=cwd).wait())

    @staticmethod
    def exit_if_error(error_no: int) -> int:
        if error_no:
            sys.exit(error_no)
        return error_no

    @staticmethod
    def install_py_requirements(path_depot: str, return_cmd: bool = False) -> List[str]:
        path_requirements = path_join(path_depot, "requirements.txt")
        if path_exists(path_requirements):
            cmd = [
                PIP_EXEC,
                "install",
                "-q",
                "--no-input",
                "--disable-pip-version-check",
                "--no-python-version-warning",
                "-r",
                path_requirements,
            ]
            if not return_cmd:
                AddonsInstaller.exec_cmd(cmd, True)
            else:
                return cmd
        else:
            _logger.debug("No requirements.txt founded in %s", path_requirements)

    @staticmethod
    def install_npm_package(path_depot: str, return_cmd: bool = False) -> List[str]:
        path_npm = path_join(path_depot, "package.json")
        if path_exists(path_npm):
            cmd = [NPM_EXEC, "install", "-g", path_npm]
            if not return_cmd:
                AddonsInstaller.exec_cmd(cmd, True)
            else:
                return cmd
        else:
            _logger.debug("No package.json founded in %s", path_npm)

    @staticmethod
    def install(addons: OdooAddonsDef, return_cmd: bool = False) -> List[List[str]]:
        """
        Clone the given addons and install required dependencies
        Sys Exit with error code when errors
        Args:
            addons: The list of addons to install
            return_cmd: if True, does not perform actual cloning, return only the commands to perform it

        Returns:

        """
        _logger.info(f"install {addons.name} in {addons.name}")
        cmd_list = []
        try:
            for cmd in addons.install_cmd():
                if not return_cmd:
                    AddonsInstaller.exec_cmd(cmd, force_log=True)
                else:
                    cmd_list.append(cmd)
            cmd_list.append(AddonsInstaller.install_py_requirements(addons.addons_path, return_cmd=return_cmd))
            cmd_list.append(AddonsInstaller.install_npm_package(addons.addons_path, return_cmd=return_cmd))
            return [cmd for cmd in cmd_list if cmd]  # remove None and empty
        except Exception as e:
            _logger.exception("Error", exc_info=e)
            sys.exit(1)
