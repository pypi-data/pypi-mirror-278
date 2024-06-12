import unittest

from src.addons_installer.addons_installer import AddonsFinder, AddonsInstaller
from src.addons_installer.git_addons import LegacyDepotGit


class TestLegacyDepotGit(unittest.TestCase):
    def test_legacy_depot_git(self):
        git_addons = LegacyDepotGit("")
        result = git_addons.extract(
            {"DEPOT_GIT": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git"}
        )
        self.assertEqual(result.name, "DEPOT_GIT")
        self.assertEqual(result.addons_path, "/odoo/addons/depot_git")

    def test_legacy_depot_git_clone_path(self):
        git_addons = LegacyDepotGit("")
        result = git_addons.extract(
            {
                "DEPOT_GIT_CLONE_PATH": "/depot_clone_path",
                "DEPOT_GIT": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            }
        )
        self.assertEqual(result.name, "DEPOT_GIT")
        self.assertEqual(result.addons_path, "/depot_clone_path")

        result = git_addons.extract(
            {
                "ADDONS_GIT_DEFAULT_CLONE_PATH": "/default_clone_path",
                "DEPOT_GIT": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            }
        )
        self.assertEqual(result.name, "DEPOT_GIT")
        self.assertEqual(result.addons_path, "/default_clone_path/depot_git")

        git_addons = LegacyDepotGit("2")
        result = git_addons.extract(
            {
                "ADDONS_GIT_DEFAULT_CLONE_PATH": "/default_clone_path",
                "DEPOT_GIT2_CLONE_PATH": "/depot2_clone_path",
                "DEPOT_GIT2": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            }
        )
        self.assertEqual(result.name, "DEPOT_GIT2")
        self.assertEqual(result.addons_path, "/depot2_clone_path")

    def test_01_legacy_discover(self):
        env_vars = {
            "DEPOT_GIT": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT):$(HTTPS_PASSWORD_DEPOT_GIT)@gitlab.fr/my_project.git",
            "DEPOT_GIT2": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT2):$(HTTPS_PASSWORD_DEPOT_GIT2)@gitlab.fr/my_project2.git",
            "DEPOT_GIT3": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT3):$(HTTPS_PASSWORD_DEPOT_GIT3)@gitlab.fr/my_project3.git",
            "DEPOT_GIT_4": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT3):$(HTTPS_PASSWORD_DEPOT_GIT3)@gitlab.fr/my_project3.git",
        }
        addons = AddonsFinder.parse_env(env_vars)
        self.assertEqual(3, len(addons), "3 DEPOT should be found [DEPOT_GIT, DEPOT_GIT2, DEPOT_GIT3]")

    def test_01_return_cmd(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_CLONE_PATH": "/odoo/addons",
            "HTTPS_USER_DEPOT_GIT": "user",
            "HTTPS_PASSWORD_DEPOT_GIT": "password",
            "HTTPS_USER_DEPOT_GIT2": "user2",
            "HTTPS_PASSWORD_DEPOT_GIT2": "password2",
            "HTTPS_USER_DEPOT_GIT3": "user3",
            "HTTPS_PASSWORD_DEPOT_GIT3": "password3",
            "DEPOT_GIT": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT):$(HTTPS_PASSWORD_DEPOT_GIT)@gitlab.fr/my_project.git",
            "DEPOT_GIT2": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT2):$(HTTPS_PASSWORD_DEPOT_GIT2)@gitlab.fr/my_project2.git",
            "DEPOT_GIT3": "-b 16.0 --single-branch --depth=1 https://$(HTTPS_USER_DEPOT_GIT3):$(HTTPS_PASSWORD_DEPOT_GIT3)@gitlab.fr/my_project3.git",
        }
        for number in ["", "2", "3"]:
            addon = LegacyDepotGit(number).extract(env_vars)
            with self.subTest(f"For depot_git => {number} [{addon.name}]"):
                cmd = AddonsInstaller.install(addon, return_cmd=True)
                self.assertEqual(
                    cmd,
                    [
                        [
                            "git",
                            "clone",
                            "-b",
                            "16.0",
                            "--single-branch",
                            "--depth=1",
                            f"https://user{number}:password{number}@gitlab.fr/my_project{number}.git",
                            f"/odoo/addons/depot_git{number}",
                        ]
                    ],
                )

    def test_legacy_depot_git_evaluate(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_CLONE_PATH": "/odoo/addons",
            "HTTPS_USER_DEPOT_GIT": "user",
            "HTTPS_PASSWORD_DEPOT_GIT": "password",
            "HTTPS_USER_DEPOT_GIT2": "user2",
            "HTTPS_PASSWORD_DEPOT_GIT2": "password2",
            "HTTPS_USER_DEPOT_GIT3": "user3",
            "HTTPS_PASSWORD_DEPOT_GIT3": "password3",
            "DEPOT_GIT": "https://$(HTTPS_USER_DEPOT_GIT):$(HTTPS_PASSWORD_DEPOT_GIT)@gitlab.fr/my_project.git",
            "DEPOT_GIT2": "https://$(HTTPS_USER_DEPOT_GIT2):$(HTTPS_PASSWORD_DEPOT_GIT2)@gitlab.fr/my_project2.git",
            "DEPOT_GIT3": "https://$(HTTPS_USER_DEPOT_GIT3):$(HTTPS_PASSWORD_DEPOT_GIT3)@gitlab.fr/my_project3.git",
        }
        for number in ["", "2", "3"]:
            with self.subTest(f"For depot_git => [{number}]"):
                git_addons = LegacyDepotGit(number)
                res = git_addons.extract(env_vars)
                self.assertEqual(
                    res.value_clone,
                    f"https://user{number}:password{number}@gitlab.fr/my_project{number}.git",
                )

    def test_legacy_depot_git_numbered(self):
        git_addons = LegacyDepotGit("")
        env = {
            "ADDONS_GIT_DEFAULT_CLONE_PATH": "/odoo/addons",
            "DEPOT_GIT": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            "DEPOT_GIT2": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            "DEPOT_GIT3": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            "DEPOT_GIT4": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            "DEPOT_GIT5": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
            "DEPOT_GIT6": "-b master --single-branch --depth=1 git@gitlab.ndp-systemes.fr:odoo/v15/issues.git",
        }
        for number in [""] + list(map(str, range(2, 10))):
            with self.subTest(f"For debot_git => [{number}]"):
                git_addons = LegacyDepotGit(number)
                result = git_addons.extract(env)
                name = "depot_git"
                if number:
                    self.assertEqual(git_addons.NAME.full_key, "DEPOT_GIT" + number)
                    name = name + number
                else:
                    self.assertEqual(git_addons.NAME.full_key, "DEPOT_GIT")

                self.assertEqual(result.name, git_addons.NAME.full_key)
                self.assertEqual(result.addons_path, "/odoo/addons/" + name)
