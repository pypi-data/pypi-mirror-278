import unittest

from src.addons_installer.addons_installer import AddonsFinder
from src.addons_installer.api import BaseAddonsResult, OdooAddonsDef
from src.addons_installer.git_addons import GitOdooAddons, GitOdooAddonsResult
from src.addons_installer.local_addons import LocalOdooAddons


class TestAddonsFinder(unittest.TestCase):
    def test_try_parse_key_local(self):
        res = AddonsFinder.try_parse_key("ADDONS_LOCAL_MY_PROJECT")
        self.assertIsNotNone(res)
        self.assertEqual(type(res), LocalOdooAddons)
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", res.base_key)
        self.assertEqual("MY_PROJECT", res.identifier)
        self.assertEqual("ADDONS_LOCAL", res.prefix)

    def test_try_parse_key_git(self):
        res = AddonsFinder.try_parse_key("ADDONS_GIT_MY_PROJECT")
        self.assertIsNotNone(res)
        self.assertEqual(type(res), GitOdooAddons)
        self.assertEqual("ADDONS_GIT_MY_PROJECT", res.base_key)
        self.assertEqual("MY_PROJECT", res.identifier)
        self.assertEqual("ADDONS_GIT", res.prefix)

    def test_try_parse_key_none(self):
        res = AddonsFinder.try_parse_key("ADDONS_MY_PROJECT")
        self.assertIsNone(res)

    def test_parse_env_empty(self):
        """No default value returned"""
        addons_definitions = AddonsFinder.parse_env({})
        self.assertFalse(addons_definitions)

    def test_parse_env_odoo_path(self):
        addons_definitions = AddonsFinder.parse_env({"ODOO_PATH": "/odoo"})
        self.assertEqual(2, len(addons_definitions))
        names = {"ADDONS_LOCAL_SRC_ODOO_ADDONS", "ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS"}
        self.assertEqual(names, set(map(lambda it: it.name, addons_definitions)))
        # order is not valid in set, so we do a swap if needed.
        base_addon, addons = addons_definitions
        if base_addon.name == "ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS":
            addons, base_addon = addons_definitions

        self.assertEqual("ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS", addons.name)
        self.assertEqual("ADDONS_LOCAL_SRC_ODOO_ADDONS", base_addon.name)
        self.assertEqual(type(base_addon), BaseAddonsResult)
        self.assertEqual(type(addons), BaseAddonsResult)
        self.assertEqual("/odoo/odoo/addons", addons.addons_path)
        self.assertEqual("/odoo/odoo/odoo/addons", base_addon.addons_path)
        self.assertEqual([], base_addon.install_cmd())
        self.assertEqual([], addons.install_cmd())

    def test_parse_env_false_value(self):
        addons_definitions = AddonsFinder.parse_env({"ADDONS_GIT_MODULES": str(False)})
        self.assertEqual(0, len(addons_definitions))
        addons_definitions = AddonsFinder.parse_env({"ADDONS_LOCAL_MODULES": str(False)})
        self.assertEqual(0, len(addons_definitions))

    def test_parse_env_git_public(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(1, len(results))
        result = results.pop()
        self.assertIsInstance(result, GitOdooAddonsResult)
        self.assertEqual("my-project", result.git_path)
        self.assertFalse(result.branch)
        self.assertEqual("/odoo/addons/my-project", result.clone_path)
        self.assertSetEqual({"--depth=1", "--quiet", "--single-branch"}, set(result.pull_options))
        self.assertIsNone(result.https_login)
        self.assertIsNone(result.https_password)
        self.assertEqual("public", result.protocole)
        self.assertEqual("gitlab.com", result.server)
        self.assertEqual("https://%(server)s/%(git_path)s.git", result.format)
        self.assertEqual("https://gitlab.com/my-project.git", result.git_url)
        install_cmds = result.install_cmd()
        arg_cmd = [
            "--depth=1",
            "--quiet",
            "--single-branch",
            "https://gitlab.com/my-project.git",
        ]
        self.assertListEqual(arg_cmd, result.arg_cmd())
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertListEqual(["git", "clone"] + arg_cmd + ["/odoo/addons/my-project"], install_cmd)

    def test_parse_env_git_pull_option_include_default(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
            "ADDONS_GIT_MY_PROJECT_PULL_OPTIONS": "--opt1,...,--opt2",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(1, len(results))
        result = results.pop()
        self.assertIsInstance(result, GitOdooAddonsResult)
        self.assertSetEqual({"--depth=1", "--quiet", "--single-branch", "--opt2", "--opt1"}, set(result.pull_options))
        install_cmds = result.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertEqual(9, len(install_cmd))
        self.assertEqual(
            [
                "git",
                "clone",
                "--opt1",
                "--depth=1",
                "--quiet",
                "--single-branch",
                "--opt2",
                "https://gitlab.com/my-project.git",
                "/odoo/addons/my-project",
            ],
            install_cmd,
        )

    def test_parse_env_git_pull_option(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
            "ADDONS_GIT_MY_PROJECT_PULL_OPTIONS": "--bare",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(1, len(results))
        result = results.pop()
        self.assertIsInstance(result, GitOdooAddonsResult)
        self.assertSetEqual({"--bare"}, set(result.pull_options))
        install_cmds = result.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertEqual(5, len(install_cmd))
        self.assertEqual(
            [
                "git",
                "clone",
                "--bare",
                "https://gitlab.com/my-project.git",
                "/odoo/addons/my-project",
            ],
            install_cmd,
        )

    def test_parse_env_default_clone_path(self):
        def assert_result(result):
            self.assertEqual("addons/my-project", result.git_path)
            self.assertFalse(result.branch)
            self.assertEqual("/opt/clone_path/my_project", result.clone_path)
            self.assertSetEqual({"--depth=1", "--quiet", "--single-branch"}, set(result.pull_options))
            self.assertEqual("public", result.protocole)
            self.assertEqual("gitlab.com", result.server)
            self.assertEqual("https://%(server)s/%(git_path)s.git", result.format)
            self.assertEqual("https://gitlab.com/addons/my-project.git", result.git_url)
            arg_cmd = [
                "--depth=1",
                "--quiet",
                "--single-branch",
                "https://gitlab.com/addons/my-project.git",
            ]
            self.assertListEqual(arg_cmd, result.arg_cmd())
            install_cmds = result.install_cmd()
            self.assertEqual(1, len(install_cmds))
            install_cmd = install_cmds[0]
            self.assertListEqual(["git", "clone"] + arg_cmd + ["/opt/clone_path/my_project"], install_cmd)

        results = AddonsFinder.parse_env(
            {
                "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
                "ADDONS_GIT_MY_PROJECT": "addons/my-project",
                # Fake key, test is removed after
                "ADDONS_GIT_DEFAULT_CLONE_PATH": "/opt/clone_path",
            }
        )
        self.assertEqual(1, len(results))
        r = results.pop()
        self.assertIsInstance(r, GitOdooAddonsResult)
        assert_result(r)
        # Test with slash at the begin and end for ADDONS_GIT_MY_PROJECT and ADDONS_GIT_DEFAULT_CLONE_PATH
        results = AddonsFinder.parse_env(
            {
                "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
                "ADDONS_GIT_MY_PROJECT": "/addons/my-project/",
                # Fake key, test is removed after
                "ADDONS_GIT_DEFAULT_CLONE_PATH": "/opt/clone_path/",
            }
        )
        self.assertEqual(1, len(results))
        r = results.pop()
        self.assertIsInstance(r, GitOdooAddonsResult)
        assert_result(r)

    def test_parse_env_git_subdir(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_CLONE_PATH": "/src/path",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
            # Key to test
            "ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT": "common",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(2, len(results))
        git_addon, sub_addon = results
        self.assertIsInstance(git_addon, OdooAddonsDef)
        self.assertIsInstance(sub_addon, OdooAddonsDef)
        if git_addon.name == "ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT":
            sub_addon, git_addon = results

        self.assertIsInstance(git_addon, GitOdooAddonsResult)
        self.assertEqual("my-project", git_addon.git_path)
        self.assertFalse(git_addon.branch)
        self.assertEqual("/src/path", git_addon.clone_path)
        self.assertSetEqual({"--depth=1", "--quiet", "--single-branch"}, set(git_addon.pull_options))
        self.assertIsNone(git_addon.https_login)
        self.assertIsNone(git_addon.https_password)
        self.assertEqual("public", git_addon.protocole)
        self.assertEqual("gitlab.com", git_addon.server)
        self.assertEqual("https://%(server)s/%(git_path)s.git", git_addon.format)
        self.assertEqual("https://gitlab.com/my-project.git", git_addon.git_url)
        arg_cmd = [
            "--depth=1",
            "--quiet",
            "--single-branch",
            "https://gitlab.com/my-project.git",
        ]
        self.assertListEqual(arg_cmd, git_addon.arg_cmd())
        install_cmds = git_addon.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertListEqual(["git", "clone"] + arg_cmd + ["/src/path"], install_cmd)

        self.assertIsInstance(sub_addon, BaseAddonsResult)
        self.assertEqual("ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT", sub_addon.name)
        self.assertEqual("/src/path/common", sub_addon.addons_path)

    def test_parse_env_priority_local_over_git(self):
        env_vars = {
            "ADDONS_LOCAL_MY_PROJECT": "/src/my-project",
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(1, len(results))
        local_addons = results.pop()
        self.assertIsInstance(local_addons, BaseAddonsResult)
        self.assertEqual("/src/my-project", local_addons.addons_path)
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", local_addons.name)
        self.assertFalse(local_addons.install_cmd())

    def test_parse_env_priority_local_over_git_2(self):
        env_vars = {
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_LOCAL_MY_PROJECT": "/src/my-project",
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(1, len(results))
        local_addons = results.pop()
        self.assertIsInstance(local_addons, BaseAddonsResult)
        self.assertEqual("/src/my-project", local_addons.addons_path)
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", local_addons.name)
        self.assertFalse(local_addons.install_cmd())

    def test_parse_env_multi_repo(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT": "common-modules",
            "ADDONS_LOCAL_MY_SECOND_PROJECT": "/path/second/projet",
            "ADDONS_SUBDIR_LOCAL_INVOICE_OF_MY_SECOND_PROJECT": "invoice_modules",
            "DEPOT_GIT": "full_command",
            "DEPOT_GIT2": "full_command",
            "DEPOT_GIT3": "full_command",
            "DEPOT_GIT_4": "full_command",  # Not valid
        }
        results = AddonsFinder.parse_env(env_vars)
        self.assertEqual(7, len(results))
