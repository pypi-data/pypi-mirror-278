from os.path import abspath, expanduser
from os.path import join as path_join
from typing import Dict

from .api import ABCSubDirAddons, AddonsSuffix, BaseAddonsResult


class LocalOdooAddons(AddonsSuffix):
    """
    This is a local Addons available on host. You need to declare an env var like this
    `"ADDONS_LOCAL_<MY_ADDONS>"="/path/to/addons"`.
    If you want you can make the path relative with a key `"ADDONS_LOCAL_<MY_ADDONS>_BASE_PATH"="/base/path"`
    Attributes:
        BASE_PATH: The key to retrieve the path where to find the Addons key format : `base_key` + "_" + "BASE_PATH`
    """

    def __init__(self, base_key: str):
        super(LocalOdooAddons, self).__init__(base_key)
        self.BASE_PATH = self.create_key("BASE_PATH", default="/")

    @property
    def prefix(self):
        return "ADDONS_LOCAL"

    def extract(self, env_vars: Dict[str, str]) -> BaseAddonsResult:
        res = self.to_dict(env_vars)
        return BaseAddonsResult(
            name=self.NAME.full_key,
            full_path=abspath(path_join(res[self.BASE_PATH], expanduser(res[self.NAME]))),
        )


class LocalSubDirOdooAddons(ABCSubDirAddons):
    _parent_type = LocalOdooAddons
    prefix = "ADDONS_SUBDIR_LOCAL"
