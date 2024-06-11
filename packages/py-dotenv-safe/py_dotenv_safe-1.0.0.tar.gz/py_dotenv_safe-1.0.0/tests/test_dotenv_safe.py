from __future__ import annotations

import os
import shutil
import unittest

from src.py_dotenv_safe.dotenv_safe import config
from src.py_dotenv_safe.missing_env_vars_error import MissingEnvVarsError


class TestDotenvSafe(unittest.TestCase):
    """
    Unit tests for the dotenv_safe module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by changing the current working directory to the tests directory
        and creating the envs directory.
        """
        cls.original_cwd = os.getcwd()
        os.chdir("./tests")
        cls.original_env = os.environ.copy()
        os.makedirs("envs", exist_ok=True)

    def setUp(self):
        """
        Set up the environment for each test by copying fixture files to the envs directory.
        """
        os.environ = self.original_env.copy()
        for file_name in os.listdir("fixtures"):
            shutil.copy(f"fixtures/{file_name}", f"envs/{file_name}")

    def tearDown(self):
        """
        Clean up after each test by removing all files in the envs directory.
        """
        for file_name in os.listdir("envs"):
            os.remove(f"envs/{file_name}")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests by changing back to the original working directory
        and removing the envs directory.
        """
        os.chdir(cls.original_cwd)
        shutil.rmtree("tests/envs")

    def test_config_success(self):
        """
        Test the config function with a valid environment file.
        """
        result = config({"examplePath": "envs/.env.success", "dotenvPath": "envs/.env"})
        self.assertIsNotNone(result)

    def test_config_allow_empty_values(self):
        """
        Test the config function allowing empty values.
        """
        result = config(
            {
                "examplePath": "envs/.env.allowEmpty",
                "dotenvPath": "envs/.env",
                "allowEmptyValues": True,
            }
        )
        self.assertIsNotNone(result)

    def test_config_no_dotenv(self):
        """
        Test the config function without a dotenv file.
        """
        os.environ["HELLO"] = "WORLD"
        result = config({"examplePath": "envs/.env.noDotEnv"})
        self.assertIsNotNone(result)

    def test_config_missing_variable(self):
        """
        Test the config function with a missing environment variable.
        """
        with self.assertRaises(MissingEnvVarsError):
            config({"examplePath": "envs/.env.fail", "dotenvPath": "envs/.env"})

    def test_config_empty_variable_not_allowed(self):
        """
        Test the config function with an empty variable not allowed.
        """
        with self.assertRaises(MissingEnvVarsError):
            config(
                {
                    "examplePath": "envs/.env.allowEmpty",
                    "dotenvPath": "envs/.env",
                    "allowEmptyValues": False,
                }
            )

    def test_config_missing_variable_allow_empty(self):
        """
        Test the config function with a missing variable allowing empty values.
        """
        with self.assertRaises(MissingEnvVarsError):
            config(
                {
                    "examplePath": "envs/.env.fail",
                    "dotenvPath": "envs/.env",
                    "allowEmptyValues": True,
                }
            )

    def test_config_no_dotenv_parsed(self):
        """
        Test the config function with no dotenv file parsed.
        """
        os.environ["HELLO"] = "fromTheOtherSide"
        result = config({"examplePath": "envs/.env.noDotEnv"})
        self.assertEqual(result["parsed"], {})
        self.assertEqual(result["required"], {})
        self.assertIn("error", result)

    def test_config_no_overwrite_env(self):
        """
        Test the config function to ensure it does not overwrite existing environment variables.
        """
        os.environ["HELLO"] = "fromTheOtherSide"
        result = config({"examplePath": "envs/.env.success", "dotenvPath": "envs/.env"})
        self.assertEqual(os.getenv("HELLO"), "fromTheOtherSide")
        self.assertEqual(result["required"], {"HELLO": "fromTheOtherSide"})

    def test_missing_env_vars_error(self):
        """
        Test raising and catching the MissingEnvVarsError.
        """
        try:
            raise MissingEnvVarsError(
                False, ".env", ".env.example", ["FOO", "BAR"], None
            )
        except MissingEnvVarsError as e:
            self.assertIn("FOO", e.message)
            self.assertIn("BAR", e.message)

    def test_config_parsed_env(self):
        """
        Test the config function to ensure environment variables are parsed correctly.
        """
        result = config(
            {
                "examplePath": "envs/.env.allowEmpty",
                "dotenvPath": "envs/.env",
                "allowEmptyValues": True,
            }
        )
        self.assertEqual(result["parsed"], {"HELLO": "world", "EMPTY": ""})


if __name__ == "__main__":
    unittest.main()
