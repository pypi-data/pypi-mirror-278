from __future__ import annotations

import logging
from os.path import exists as path_exists
from os.path import expanduser
from os.path import join as path_join
from pathlib import Path
from typing import Dict, List

from .api import (
    ABCSubDirAddons,
    AddonsSuffix,
    BaseAddonsResult,
    KeySuffix,
    OdooAddonsDef,
)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class GitOdooAddons(AddonsSuffix):
    """
    Represent a Git remote url to clone to get Odoo Addons.

    """

    PROTOCOLE_HTTPS = "https"
    PROTOCOLE_SSH = "ssh"
    PROTOCOLE_PUBLIC = "public"
    FORMAT_GIT_CLONE = {
        PROTOCOLE_HTTPS: "https://%(login)s:%(password)s@%(server)s/%(git_path)s.git",
        PROTOCOLE_SSH: "git@%(server)s:%(git_path)s.git",
        PROTOCOLE_PUBLIC: "https://%(server)s/%(git_path)s.git",
    }

    def __init__(self, base_key):
        super(GitOdooAddons, self).__init__(base_key)
        self.BRANCH = self.create_key("BRANCH")
        self.CLONE_PATH = self.create_key("CLONE_PATH")
        self.PULL_OPTIONS = self.create_key("PULL_OPTIONS", default="--depth=1,--quiet,--single-branch")
        self.HTTPS_LOGIN = self.create_key("HTTPS_LOGIN")
        self.HTTPS_PASSWORD = self.create_key("HTTPS_PASSWORD")
        self.PROTOCOLE = self.create_key("PROTOCOLE", default=self.PROTOCOLE_PUBLIC)
        self.SERVER = self.create_key("SERVER")  # TODO rename key with SERVER_GIT instead of SERVER

    @property
    def prefix(self):
        return "ADDONS_GIT"

    def extract(self, env_vars: Dict[str, str]) -> GitOdooAddonsResult:
        res = self.to_dict(env_vars)
        self._apply_check(env_vars, res)

        # Remove the '/' at the end and the beginning of the name '/p1/p2' become 'p1/p2'
        res[self.NAME] = res[self.NAME].strip("/")

        protocole = self._get_protocole(env_vars, res)
        clone_path = self._get_clone_path(env_vars, res)
        pull_option = self._get_pull_option(res)

        if self.PROTOCOLE_HTTPS != protocole:
            res.pop(self.HTTPS_LOGIN, False)
            res.pop(self.HTTPS_PASSWORD, False)

        return GitOdooAddonsResult(
            name=self.identifier,
            git_path=res[self.NAME],
            branch=res[self.BRANCH],
            clone_path=clone_path,
            pull_options=pull_option,
            https_login=res.get(self.HTTPS_LOGIN),
            https_password=res.get(self.HTTPS_PASSWORD),
            protocole=protocole,
            server=res[self.SERVER],
        )

    def _get_protocole(self, env_vars: Dict[str, str], res: Dict[KeySuffix, str]):
        if (
            not self.PROTOCOLE.get_value(env_vars, with_default=False)
            and res[self.HTTPS_LOGIN]
            and res[self.HTTPS_PASSWORD]
        ):
            return self.PROTOCOLE_HTTPS
        return res[self.PROTOCOLE]

    def _apply_check(self, env_vars: Dict[str, str], res: Dict[KeySuffix, str]):
        if not res[self.SERVER]:
            raise ValueError(
                "Not git server is provided, key [%s] or [%s]" % (self.SERVER.full_key, self.SERVER.default_key)
            )
        if res[self.PROTOCOLE] not in self.FORMAT_GIT_CLONE.keys():
            raise ValueError(
                "The selected protocole %s is not supported, possible values are %s"
                % (res[self.PROTOCOLE], sorted(list(self.FORMAT_GIT_CLONE.keys())))
            )
        if self.PROTOCOLE_SSH == res[self.PROTOCOLE]:
            raise ValueError("Protocole [%s] not supported for the moment" % self.PROTOCOLE_SSH)

        protocole = self._get_protocole(env_vars, res)
        if self.PROTOCOLE_HTTPS == protocole:
            if not res[self.HTTPS_LOGIN] or not res[self.HTTPS_PASSWORD]:
                raise ValueError(
                    "Please add %s and %s var in your environment when you use [%s] has git protocole"
                    % (
                        self.HTTPS_LOGIN.full_key,
                        self.HTTPS_PASSWORD.full_key,
                        self.PROTOCOLE_HTTPS,
                    )
                )

    def _get_clone_path(self, env_vars, res):
        # type: (Dict[str, str], Dict[KeySuffix, str]) -> str
        if self.CLONE_PATH.default_key in env_vars and self.CLONE_PATH.full_key not in env_vars:
            # If default key in env_vars but not dedicated key then we add identifier in lower case to the clone path
            return path_join(res[self.CLONE_PATH], self.identifier.lower())
        return res[self.CLONE_PATH]

    def _get_pull_option(self, res):
        pull_option = res[self.PULL_OPTIONS]
        if isinstance(pull_option, str):
            pull_option = pull_option.split(",")
        if "..." in pull_option:
            idx = pull_option.index("...")
            pull_option.pop(idx)
            pull_option[idx:idx] = self.PULL_OPTIONS.default_value.split(",")
        return pull_option


class GitOdooAddonsResult(OdooAddonsDef):
    def __init__(
        self,
        name,
        git_path,
        branch,
        clone_path,
        pull_options,
        https_login,
        https_password,
        protocole,
        server,
    ):
        super(GitOdooAddonsResult, self).__init__(name)
        self.git_path = git_path
        self.branch = branch
        if not clone_path:
            clone_path = path_join("/", "odoo", "addons", git_path.lower())
        if not clone_path:
            clone_path = path_join(clone_path, git_path.lower())
        self.clone_path = expanduser(clone_path)
        self.pull_options = pull_options
        self.https_login = https_login
        self.https_password = https_password
        self.protocole = protocole
        self.server = server
        self.format = GitOdooAddons.FORMAT_GIT_CLONE[protocole]

    def install_cmd(self) -> List[List[str]]:
        if path_exists(self.clone_path):
            _logger.info("Path %s not empty to clone %s", self.clone_path, self)
            return []
        clone_cmd = ["git", "clone"]
        clone_cmd.extend(self.arg_cmd())
        clone_cmd.append(self.clone_path)
        return [clone_cmd]

    def arg_cmd(self) -> List[str]:
        clone_cmd = []
        if self.pull_options:
            clone_cmd.extend(self.pull_options)
        if self.branch:
            clone_cmd.append("-b")
            clone_cmd.append(self.branch)
        clone_cmd.append(self.git_url)
        return clone_cmd

    @property
    def addons_path(self) -> str:
        return self.clone_path

    @property
    def git_url(self) -> str:
        return self.format % {
            "login": self.https_login,
            "password": self.https_password,
            "server": self.server,
            "git_path": self.git_path,
        }


class GitSubDirOdooAddons(ABCSubDirAddons):
    _parent_type = GitOdooAddons

    @property
    def prefix(self):
        return "ADDONS_SUBDIR_GIT"

    def extract(self, env_vars: Dict[str, str]) -> BaseAddonsResult:
        res = self.to_dict(env_vars)
        git_res = self.parent_addons.extract(env_vars)
        full_path = path_join(git_res.addons_path, res[self.NAME])
        return BaseAddonsResult(name=self.NAME.full_key, full_path=full_path)


class LegacyDepotGitKey(KeySuffix):
    @property
    def full_key(self) -> str:
        return self.prefix + self.base_key + (self.name and "_" + self.name or "")


class LegacyDepotGit(AddonsSuffix):
    def __init__(self, base_key: str):
        super().__init__(base_key)
        self.CLONE_PATH = self.create_key("CLONE_PATH")

    def create_key(self, name: str, default: str = None, have_default: bool = True):
        key = LegacyDepotGitKey(addons=self, name=name, default=default, have_default=have_default)
        self._key_registry[name] = key
        return key

    @property
    def prefix(self):
        return "DEPOT_GIT"

    def extract(self, env_vars: Dict[str, str]) -> LegacyDepotGitResult:
        res = self.to_dict(env_vars)
        clone_path = res[self.CLONE_PATH]
        if not clone_path:
            base_clone_path_dir = env_vars.get(GitOdooAddons("").CLONE_PATH.default_key)
            if not base_clone_path_dir:
                base_clone_path_dir = "/odoo/addons"
            clone_path = Path(base_clone_path_dir).joinpath(self.NAME.full_key.lower())

        #
        value_clone = res[self.NAME]
        key_user = f"HTTPS_USER_{self.NAME.full_key}"
        if key_user in env_vars:
            value_clone = value_clone.replace(f"$({key_user})", env_vars[key_user])
        key_password = f"HTTPS_PASSWORD_{self.NAME.full_key}"
        if key_password in env_vars:
            value_clone = value_clone.replace(f"$({key_password})", env_vars[key_password])
        return LegacyDepotGitResult(self.NAME.full_key, clone_path=str(clone_path), value_clone=value_clone)


class LegacyDepotGitResult(OdooAddonsDef):
    def __init__(
        self,
        name,
        clone_path,
        value_clone,
    ):
        super(LegacyDepotGitResult, self).__init__(name)
        self.clone_path = clone_path
        self.value_clone = value_clone

    @property
    def addons_path(self) -> str:
        return self.clone_path

    def install_cmd(self) -> List[List[str]]:
        if path_exists(self.clone_path):
            _logger.info("Path %s not empty to clone %s", self.clone_path, self)
            return []
        clone_cmd = ["git", "clone"]
        clone_cmd.extend(self.arg_cmd())
        clone_cmd.append(self.clone_path)
        return [clone_cmd]

    def arg_cmd(self) -> List[str]:
        return self.value_clone.split(" ")
