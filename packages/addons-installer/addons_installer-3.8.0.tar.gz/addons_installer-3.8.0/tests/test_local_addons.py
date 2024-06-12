import unittest

from src.addons_installer.local_addons import LocalOdooAddons, LocalSubDirOdooAddons


class TestLocalAddonsSuffix(unittest.TestCase):
    def test_local(self):
        suffix = LocalOdooAddons("ADDONS_LOCAL_MY_PROJECT")
        self.assertEqual("MY_PROJECT", suffix.identifier)
        self.assertTrue(suffix.is_valid())
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", suffix.NAME.full_key)
        self.assertIsNone(suffix.NAME.default_key)

        self.assertEqual("ADDONS_LOCAL_MY_PROJECT_BASE_PATH", suffix.BASE_PATH.full_key)
        self.assertEqual("ADDONS_LOCAL_DEFAULT_BASE_PATH", suffix.BASE_PATH.default_key)

    def test_local_sub(self):
        suffix_of = LocalSubDirOdooAddons("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT")
        self.assertEqual("ADDONS_SUBDIR_LOCAL", suffix_of.prefix)
        self.assertEqual("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT", suffix_of.NAME.full_key)
        self.assertEqual("TEST_OF_MY_PROJECT", suffix_of.identifier)
        self.assertEqual("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT", suffix_of.base_key)
        self.assertTrue(suffix_of.is_valid())
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", suffix_of.parent_addons.NAME.full_key)
        self.assertIsNone(suffix_of.NAME.default_key)

        self.assertEqual("ADDONS_LOCAL_MY_PROJECT_BASE_PATH", suffix_of.parent_addons.BASE_PATH.full_key)
        self.assertEqual("ADDONS_LOCAL_DEFAULT_BASE_PATH", suffix_of.parent_addons.BASE_PATH.default_key)

        result = suffix_of.extract(
            {
                "ADDONS_LOCAL_TEST": "/path/to/test",
                "ADDONS_LOCAL_MY_PROJECT": "/path/to/my_project",
                "ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT": "/subdir_of_my_project",
            }
        )

        self.assertEqual("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT", result.name)
        self.assertEqual("/path/to/my_project/subdir_of_my_project", result.addons_path)

        result = suffix_of.extract(
            {
                "ADDONS_LOCAL_MY_PROJECT": "/path/to/my_project/",
                "ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT": "/subdir_of_my_project",
            }
        )

        self.assertEqual("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT", result.name)
        self.assertEqual("/path/to/my_project/subdir_of_my_project", result.addons_path)

        result = suffix_of.extract(
            {
                "ADDONS_LOCAL_MY_PROJECT": "/path/to/my_project",
                "ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT": "subdir_of_my_project",
            }
        )

        self.assertEqual("ADDONS_SUBDIR_LOCAL_TEST_OF_MY_PROJECT", result.name)
        self.assertEqual("/path/to/my_project/subdir_of_my_project", result.addons_path)

    def test_local_addons_struct(self):
        addons = LocalOdooAddons("MY_MODULE")
        self.assertEqual(2, len(addons.get_suffix_keys()))
        self.assertEqual("MY_MODULE", addons.identifier)
        # Ensure LocalOdooAddons and all the keySuffix
        self.assertEqual(addons.ADDONS_SUFFIX_EXCLUDE, "EXCLUDE")

        self.assertEqual(addons.prefix, "ADDONS_LOCAL")
        self.assertEqual(addons.NAME.prefix, addons.prefix)
        self.assertEqual(addons.BASE_PATH.prefix, addons.prefix)

    def test_name_key(self):
        addons = LocalOdooAddons("MY_MODULE")
        self.assertEqual(addons.NAME.full_key, "ADDONS_LOCAL_MY_MODULE")
        self.assertIsNone(addons.NAME.default_key, "This key is mandatory, so no default are available")
        self.assertEqual(addons.NAME.base_key, "MY_MODULE")
        self.assertEqual(addons.NAME.name, "", "The name key don't have name")
        self.assertEqual(addons.NAME.have_default, False)
        env_to_assert_name = {
            "ADDONS_LOCAL_MY_MODULE": "/path/to/my_module",
            "ADDONS_LOCAL_MY_MODULE_DEFAULT": "/default/path/to/my_module",
        }
        self.assertEqual(addons.NAME.get_value(env_to_assert_name, with_default=False), "/path/to/my_module")
        self.assertEqual(addons.NAME.get_value(env_to_assert_name, with_default=True), "/path/to/my_module")

    def test_base_path_key(self):
        addons = LocalOdooAddons("MY_MODULE")
        self.assertEqual(addons.BASE_PATH.name, "BASE_PATH", "The name key don't have name")
        self.assertEqual(addons.BASE_PATH.base_key, "MY_MODULE")
        self.assertEqual(addons.BASE_PATH.full_key, "ADDONS_LOCAL_MY_MODULE_BASE_PATH", "prefix + base_key + name")
        self.assertEqual(
            addons.BASE_PATH.default_key, "ADDONS_LOCAL_DEFAULT_BASE_PATH", "Default key are not linked to the base_key"
        )
        self.assertEqual(addons.BASE_PATH.default_value, "/", "Default in code should be `/`")
        self.assertEqual(addons.BASE_PATH.have_default, True)
        self.assertEqual(addons.BASE_PATH.get_value({}, with_default=True), "/")
        self.assertIsNone(addons.BASE_PATH.get_value({}, with_default=False))
        env_to_assert_base_path = {
            "ADDONS_LOCAL_MY_MODULE_BASE_PATH": "/base/path",
            "ADDONS_LOCAL_DEFAULT_BASE_PATH": "/default/path",
        }
        self.assertEqual(addons.BASE_PATH.get_value(env_to_assert_base_path, with_default=True), "/base/path")
        self.assertEqual(addons.BASE_PATH.get_value(env_to_assert_base_path, with_default=False), "/base/path")
        env_to_assert_base_path = {
            "ADDONS_LOCAL_DEFAULT_BASE_PATH": "/default/path",
        }
        self.assertEqual(addons.BASE_PATH.get_value(env_to_assert_base_path, with_default=True), "/default/path")
        self.assertEqual(addons.BASE_PATH.get_value(env_to_assert_base_path, with_default=False), "/default/path")

    def test_absolute_path(self):
        res = LocalOdooAddons("MY_MODULE").extract(
            {
                "ADDONS_LOCAL_MY_MODULE": "/path/to/my_module",
                "ADDONS_LOCAL_MY_MODULE_BASE_PATH": "/default/path/to/my_module",
            }
        )
        self.assertEqual(res.name, "ADDONS_LOCAL_MY_MODULE")
        self.assertEqual(
            res.addons_path,
            "/path/to/my_module",
            "BASE_PATH not used because path startwith `/` so it's an absolute one",
        )
        self.assertEqual(res.install_cmd(), [])
        self.assertEqual(res.arg_cmd(), [])

    def test_default_base_path(self):
        res = LocalOdooAddons("MY_MODULE").extract(
            {
                "ADDONS_LOCAL_MY_MODULE": "to/my_module",
                "ADDONS_LOCAL_DEFAULT_BASE_PATH": "/default/path",
            }
        )
        self.assertEqual(res.name, "ADDONS_LOCAL_MY_MODULE")
        self.assertEqual(
            res.addons_path, "/default/path/to/my_module", "BASE_PATH used because path don't startwith `/`"
        )
        self.assertEqual(res.install_cmd(), [])
        self.assertEqual(res.arg_cmd(), [])

    def test_base_path(self):
        addons = LocalOdooAddons("MY_MODULE")
        res = addons.extract(
            {
                "ADDONS_LOCAL_MY_MODULE": "to/my_module",
                "ADDONS_LOCAL_MY_MODULE_BASE_PATH": "/base/path",
            }
        )
        self.assertEqual(res.name, "ADDONS_LOCAL_MY_MODULE")
        self.assertEqual(res.addons_path, "/base/path/to/my_module", "BASE_PATH used because path don't startwith `/`")
        self.assertEqual(res.install_cmd(), [])
        self.assertEqual(res.arg_cmd(), [])
