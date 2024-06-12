from __future__ import annotations

import abc
import os
from typing import Dict, List, Optional, Type, TypeVar


class KeySuffix(object):
    def __init__(self, addons: AddonsSuffix, name: str, default: str = None, have_default: bool = True):
        self.name = name
        self.prefix = addons.prefix
        self.base_key = addons.identifier
        self.default_value = default
        self.have_default = have_default

    def get_value(self, env_vars: Dict[str, str], with_default: bool = True) -> Optional[str]:
        return env_vars.get(self.full_key, None) or env_vars.get(
            self.default_key, with_default and self.default_value or None
        )

    def in_env(self, env_vars: Dict[str, str], use_default_key: bool = False) -> bool:
        in_env = self.full_key in env_vars.keys()
        if not in_env and use_default_key:
            in_env = self.default_key in env_vars.keys()
        return in_env

    def _get_key(self, prefix: str, middle: str, suffix: str) -> str:
        return "_".join([s for s in [prefix, middle, suffix] if s]).upper()

    @property
    def full_key(self) -> str:
        return self._get_key(self.prefix, self.base_key, self.name)

    @property
    def default_key(self) -> Optional[str]:
        return self.have_default and self._get_key(self.prefix, AddonsSuffix.ADDONS_DEFAULT, self.name) or None

    def __repr__(self) -> str:
        return "%s(%s, default=%s)" % (type(self).__name__, self.full_key, self.default_key)


class AddonsSuffix(abc.ABC):
    ADDONS_DEFAULT = "DEFAULT"
    ADDONS_SUFFIX_EXCLUDE = "EXCLUDE"

    prefix: str = None

    def __init__(self, base_key: str):
        super(AddonsSuffix, self).__init__()
        assert self.prefix, "Set the prefix attribute in %s" % type(self)
        self.base_key = base_key
        self._key_registry: Dict[str, KeySuffix] = {}
        self._values = {}
        self.NAME = self.create_key("", have_default=False)

    @property
    def identifier(self) -> str:
        return self.base_key.replace(self.prefix, "").strip("_")

    @abc.abstractmethod
    def extract(self, env_vars: Dict[str, str]) -> OdooAddonsDef:
        raise NotImplementedError()

    def to_dict(self, env_vars: Dict[str, str]) -> Dict[KeySuffix, str]:
        return {key: key.get_value(env_vars) for key_name, key in self._key_registry.items()}

    def to_env_dict(self, env_vars: Dict[str, str]) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for key in self._key_registry.values():
            value = key.get_value(env_vars, with_default=True)
            if value:
                result[key.full_key] = value
        return result

    def get_suffix_keys(self) -> List[str]:
        return list(self._key_registry.keys())

    def create_key(self, name: str, default: str = None, have_default: bool = True):
        key = KeySuffix(addons=self, name=name, default=default, have_default=have_default)
        self._key_registry[name] = key
        return key

    def is_valid(self) -> bool:
        return (
            self.base_key.startswith(self.prefix)
            and not any(self.base_key.endswith(suffix) for suffix in self.get_suffix_keys() if suffix)
            and not self.base_key.endswith(self.ADDONS_SUFFIX_EXCLUDE)
            and self.NAME.full_key == self.base_key
        )

    def __repr__(self) -> str:
        return "%s(%s)" % (type(self).__name__, self.identifier)

    def __eq__(self, other: AddonsSuffix) -> bool:
        return isinstance(other, AddonsSuffix) and other.identifier == self.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


class OdooAddonsDef(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    @abc.abstractmethod
    def addons_path(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def install_cmd(self) -> List[List[str]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def arg_cmd(self) -> List[str]:
        raise NotImplementedError()


PT = TypeVar("PT", bound="AddonsSuffix")


class ABCSubDirAddons(AddonsSuffix, abc.ABC):
    parent_addons: PT

    _parent_type: Type[PT] = None

    def __init__(self, base_key: str):
        assert self._parent_type, "Set _parent_type in %s" % type(self)
        super(ABCSubDirAddons, self).__init__(base_key)
        of_ref = base_key.split("_OF_")[-1]
        self.parent_addons = None
        if of_ref and self.is_valid():
            tmp = self._parent_type("")
            key_git = tmp.prefix + "_" + of_ref
            self.parent_addons = self._parent_type(key_git)
            assert self.parent_addons.is_valid(), "The key %s is not a Addons valid key" % key_git

    def is_valid(self) -> bool:
        return super().is_valid() and "_OF_" in self.base_key

    @property
    def identifier(self) -> str:
        return super().identifier

    def extract(self, env_vars: Dict[str, str]) -> BaseAddonsResult:
        res = self.to_dict(env_vars)
        parent_extract = self.parent_addons.extract(env_vars)
        sub_path = res[self.NAME]

        if os.path.isabs(sub_path):
            sub_path = sub_path[1:]  # Remove '/' at first, removeprefix don't exist in 3.8
        full_path = os.path.join(parent_extract.addons_path, sub_path)
        return BaseAddonsResult(name=self.NAME.full_key, full_path=full_path)


class BaseAddonsResult(OdooAddonsDef):
    def __init__(self, name: str, full_path: str):
        super().__init__(name)
        self.name = name
        self._full_path = full_path

    def install_cmd(self) -> List[List[str]]:
        return []

    def arg_cmd(self) -> List[str]:
        return []

    @property
    def addons_path(self) -> str:
        return self._full_path
