import argparse
import inspect
import sys
import unittest
from typing import Any, Dict, List, Union
from unittest.mock import MagicMock

from src.addons_installer.addons_installer import AddonsFinder, AddonsInstaller
from src.addons_installer.cli import (
    _get_addons,
    _get_parser,
    _get_profiles,
    _install_addons,
    _load_profiles,
    install_from_env,
)


class TestAddonsInstaller(unittest.TestCase):
    def _assertParser(
        self, parser: argparse.ArgumentParser, env_args: Union[List[str], str], expected_values: Dict[str, Any]
    ):
        """
        Assert the parser comparing the expectedValue.
        Args:
            parser: The parser to assert
            env_vars: the command line arguments
            expected_values: The key, value to assert
        """
        self.assertTrue(parser)
        self.assertTrue(expected_values)
        args = parser.parse_args(env_args)
        for key, value in expected_values.items():
            pvalue = getattr(args, key)
            self.assertEqual(pvalue, value, f"<{key}> not equal")

    def test_01_return_cmd(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
        }
        addons = AddonsFinder.parse_env(env_vars)
        addon = addons.pop()  # reduce the list to its only element
        cmd = AddonsInstaller.install(addon, return_cmd=True)
        self.assertTrue(cmd)
        self.assertEqual(
            cmd,
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/my-project.git",
                    "/odoo/addons/my-project",
                ]
            ],
        )

    def test_02_perform_install(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
        }
        AddonsInstaller.exec_cmd = MagicMock()
        addons = AddonsFinder.parse_env(env_vars)
        addon = addons.pop()
        AddonsInstaller.install(addon)
        AddonsInstaller.exec_cmd.assert_called_with(
            [
                "git",
                "clone",
                "--depth=1",
                "--quiet",
                "--single-branch",
                "https://gitlab.com/my-project.git",
                "/odoo/addons/my-project",
            ],
            force_log=True,
        )

    def test_03_load_profiles(self):
        vars = _load_profiles(["tests/profiles/test_profile1"])
        self.assertEqual(vars["ADDONS_GIT_MY_PROJECT"], "my-project")

    def test_03bis_load_profiles(self):
        vars = _load_profiles(["tests/profiles/test_profile1", "tests/profiles/test_profile2"])
        self.assertEqual(vars["ADDONS_GIT_MY_PROJECT"], "my-project")
        self.assertEqual(vars["ADDONS_GIT_OTHER_PROJECT"], "other-project")

    def test_04_get_parser_all(self):
        parser = _get_parser()
        self._assertParser(
            parser,
            ["--all", "--profiles", "prof1,prof2"],
            expected_values={"all": True, "profiles": "prof1,prof2"},
        )

    def test_04bis_get_parser_default(self):
        parser = _get_parser()
        self._assertParser(
            parser,
            [],
            expected_values={"all": False, "install": None},
        )

    def test_05_get_parser_specific(self):
        parser = _get_parser()
        self._assertParser(
            parser,
            ["-i", "monaddons", "--profiles", "prof1,prof2"],
            expected_values={"install": "monaddons", "profiles": "prof1,prof2", "all": False},
        )

    def test_06_get_profiles(self):
        parser = _get_parser()
        self.assertEqual(
            _get_profiles(parser.parse_args(["--profiles", "prof1,prof2,prof3"]).profiles),
            ["prof1", "prof2", "prof3"],
            "commas separated list translated into list of filename",
        )

    def test_07_get_addons(self):
        self.assertEqual(
            _get_addons(_get_parser().parse_args(["-i", "COMMON15,web_truc"]).install), ["COMMON15", "WEB_TRUC"]
        )

    def test_08_cli_exists(self):
        # entry point must exist
        from src.addons_installer.cli import install_from_env

        self.assertTrue(install_from_env)
        # entrypoint has no parameters (args will be passed from command line)
        for param_name, param in inspect.signature(install_from_env).parameters.items():
            self.assertIsNot(
                param.default, inspect._empty, f"Params {param_name} on {install_from_env} must have a default value"
            )
            self.assertIsNot(
                param.default, inspect._void, f"Params {param_name} on {install_from_env} must have a default value"
            )

    def test_09__install_addons(self):
        args = _get_parser().parse_args(["-i", "COMMONO,web_truc", "--cmd-only"])
        cmd = _install_addons(
            args=args,
            env_vars={
                "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
                "ADDONS_GIT_COMMONO": "commono",
                "ADDONS_GIT_WEB_TRUC": "web_truc",
            },
            specifics_addons=["COMMONO", "WEB_TRUC"],
        )
        # we assert presence, order is not guaranteed
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )

    def test_10_cli_select_addons(self):
        restore_args = sys.argv
        sys.argv = [
            "install_from_env",
            "-i",
            "COMMONO,web_truc",
            "--cmd-only",
            "--profiles",
            "tests/profiles/test_profile3",
        ]
        cmd = install_from_env()
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )
        sys.argv = restore_args

    def test_11_cli_all_addons(self):
        restore_args = sys.argv
        sys.argv = ["install_from_env", "--all", "--profiles", "tests/profiles/test_profile3", "--cmd-only"]
        cmd = install_from_env()
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )
        sys.argv = restore_args

    def test_10_cli_select_one_addons(self):
        restore_args = sys.argv
        sys.argv = ["install_from_env", "-i", "web_truc", "--cmd-only", "--profiles", "tests/profiles/test_profile3"]
        cmd = install_from_env()
        self.assertFalse(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "-b",
                    "master",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )
        sys.argv = restore_args

    def test_12_cli_all_by_default(self):
        restore_args = sys.argv
        sys.argv = ["install_from_env", "--profiles", "tests/profiles/test_profile3", "--cmd-only"]
        cmd = install_from_env()
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )
        sys.argv = restore_args

    def test_13_cli_all_override(self):
        restore_args = sys.argv
        sys.argv = [
            "install_from_env",
            "-i",
            "web_truc",
            "--all",
            "--profiles",
            "tests/profiles/test_profile3",
            "--cmd-only",
        ]
        cmd = install_from_env()
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/commono.git",
                    "/odoo/addons/commono",
                ]
            ]
            in cmd
        )
        self.assertTrue(
            [
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--quiet",
                    "--single-branch",
                    "https://gitlab.com/web_truc.git",
                    "/odoo/addons/web_truc",
                ]
            ]
            in cmd
        )
        sys.argv = restore_args
