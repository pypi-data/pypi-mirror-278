import os
import unittest
from typing import Any, Callable

from src.addons_installer.api import KeySuffix
from src.addons_installer.git_addons import GitOdooAddons, GitOdooAddonsResult


class TestGitAddonsSuffix(unittest.TestCase):
    def setUp(self):
        self.git_addons = GitOdooAddons("MY_PROJECT")

    def test_name_suffix(self):
        self.assertEqual(8, len(self.git_addons.get_suffix_keys()))
        self.assertEqual("ADDONS_GIT_MY_PROJECT_BRANCH", self.git_addons.BRANCH.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_BRANCH", self.git_addons.BRANCH.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_CLONE_PATH", self.git_addons.CLONE_PATH.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_CLONE_PATH", self.git_addons.CLONE_PATH.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_PULL_OPTIONS", self.git_addons.PULL_OPTIONS.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_PULL_OPTIONS", self.git_addons.PULL_OPTIONS.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_PROTOCOLE", self.git_addons.PROTOCOLE.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_PROTOCOLE", self.git_addons.PROTOCOLE.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN", self.git_addons.HTTPS_LOGIN.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_HTTPS_LOGIN", self.git_addons.HTTPS_LOGIN.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD", self.git_addons.HTTPS_PASSWORD.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_HTTPS_PASSWORD", self.git_addons.HTTPS_PASSWORD.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_SERVER", self.git_addons.SERVER.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_SERVER", self.git_addons.SERVER.default_key)

    def test_extract_raise_no_server(self):
        with self.assertRaises(ValueError) as e:
            self.git_addons.extract({"ADDONS_GIT_MY_PROJECT_BRANCH": "branch_name"})
        self.assertEqual(
            "Not git server is provided, key [ADDONS_GIT_MY_PROJECT_SERVER] or [ADDONS_GIT_DEFAULT_SERVER]",
            e.exception.args[0],
        )

    def get_result(self, other_keys):
        # type: (Dict[str, str]) -> GitOdooAddonsResult
        return self.git_addons.extract(
            dict({"ADDONS_GIT_MY_PROJECT": "my-project", "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com"}, **other_keys)
        )

    def test_extract_default_value(self):
        result = self.get_result({})
        self.assertEqual("gitlab.com", result.server)
        self.assertEqual("public", result.protocole)
        self.assertFalse(result.branch)
        self.assertEqual("/odoo/addons/my-project", result.clone_path)
        self.assertIsNone(result.https_password)
        self.assertIsNone(result.https_login)
        self.assertEqual("https://%(server)s/%(git_path)s.git", result.format)
        self.assertSetEqual({"--depth=1", "--quiet", "--single-branch"}, set(result.pull_options))

    def test_extract_BRANCH(self):
        self.factory_test_extract(self.git_addons.BRANCH, "--value", lambda r: r.branch)

    def test_extract_CLONE_PATH(self):
        suffix = self.git_addons.CLONE_PATH
        value = "value"
        # self.factory_test_extract(self.suffix.CLONE_PATH, "value", lambda r: r.clone_path)
        result = self.get_result({suffix.full_key: value})
        self.assertEqual(value, result.clone_path)

        result = self.get_result({suffix.default_key: value + "_1"})
        self.assertEqual(value + "_1/my_project", result.clone_path)
        result = self.get_result(
            {
                suffix.full_key: value + "_3",
                suffix.default_key: value + "_2",
            }
        )
        self.assertEqual(value + "_3", result.clone_path)
        # Test expand user
        result = self.get_result({"ADDONS_GIT_MY_PROJECT_CLONE_PATH": "~/src"})
        self.assertEqual(os.path.expanduser("~/src"), result.clone_path)

    def test_extract_PULL_OPTIONS(self):
        self.factory_test_extract(self.git_addons.PULL_OPTIONS, "value", lambda r: r.pull_options[0])

    def test_extract_PROTOCOLE_raise(self):
        value = "wrong_value"
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": value})
        self.assertEqual(
            "The selected protocole wrong_value is not supported, possible values are ['https', 'public', 'ssh']",
            e.exception.args[0],
        )

        # Test case sensitive
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "HTTPS"})
        self.assertEqual(
            "The selected protocole HTTPS is not supported, possible values are ['https', 'public', 'ssh']",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_HTTPS_missing_values(self):
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https"})
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD "
            "var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )
        with self.assertRaises(ValueError) as e:
            self.get_result(
                {
                    "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                    "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                }
            )
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD "
            "var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )
        with self.assertRaises(ValueError) as e:
            self.get_result(
                {
                    "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                    "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
                }
            )
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD "
            "var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_HTTPS(self):
        result = self.get_result(
            {
                "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
            }
        )
        self.assertEqual(result.protocole, "https")
        self.assertEqual(result.https_login, "login")
        self.assertEqual(result.https_password, "password")
        self.assertEqual(result.format, "https://%(login)s:%(password)s@%(server)s/%(git_path)s.git")
        self.assertEqual(result.git_url, "https://login:password@gitlab.com/my-project.git")

    def test_extract_PROTOCOLE_SSH(self):
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "ssh"})
        self.assertEqual(
            "Protocole [ssh] not supported for the moment",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_PUBLIC(self):
        result = self.get_result(
            {
                "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
                # Fake key, test is removed after
                "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
                "ADDONS_GIT_MY_PROJECT_SSH_KEY": "my-key",
            }
        )
        self.assertEqual(result.protocole, "public")
        self.assertIsNone(result.https_login)
        self.assertIsNone(result.https_password)
        self.assertEqual(result.format, "https://%(server)s/%(git_path)s.git")
        self.assertEqual(result.git_url, "https://gitlab.com/my-project.git")

    def test_extract_SERVER(self):
        self.factory_test_extract(self.git_addons.SERVER, "server_git", lambda r: r.server)

    def factory_test_extract(self, suffix: KeySuffix, value: Any, getter: Callable[[GitOdooAddonsResult], Any]):
        result = self.get_result({suffix.full_key: value})
        self.assertEqual(value, getter(result))

        result = self.get_result({suffix.default_key: value + "_1"})
        self.assertEqual(value + "_1", getter(result))
        result = self.get_result(
            {
                suffix.full_key: value + "_3",
                suffix.default_key: value + "_2",
            }
        )
        self.assertEqual(value + "_3", getter(result))
