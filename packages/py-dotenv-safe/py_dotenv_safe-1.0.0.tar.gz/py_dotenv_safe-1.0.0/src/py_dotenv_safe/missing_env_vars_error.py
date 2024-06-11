from __future__ import annotations

from typing import List, Optional


class MissingEnvVarsError(Exception):
    """
    Exception raised for missing environment variables.

    Attributes:
        allow_empty_values (bool): Indicates whether empty values are allowed.
        dotenv_filename (str): The .env filename where variables are expected.
        example_filename (str): The example .env filename.
        missing_vars (list): List of missing environment variables.
        error (Exception, optional): The original exception thrown, if any.
    """

    def __init__(
        self,
        allow_empty_values: bool,
        dotenv_filename: str,
        example_filename: str,
        missing_vars: list[str],
        error: Exception | None = None,
    ):
        """
        Initialize the MissingEnvVarsError.

        Args:
            allow_empty_values (bool): Whether empty values are allowed.
            dotenv_filename (str): The .env filename.
            example_filename (str): The example .env filename.
            missing_vars (list): List of missing environment variables.
            error (Exception, optional): The original exception thrown, if any.
        """

        error_message = (
            f"The following variables were defined in {example_filename} but are not "
            f"present in the environment:\n  {', '.join(missing_vars)}\n"
            f"Make sure to add them to {dotenv_filename} or directly to the environment."
        )

        allow_empty_values_message = (
            ""
            if allow_empty_values
            else (
                "If you expect any of these variables to be empty, you can use the "
                "allow_empty_values option:\nconfig(allow_empty_values=True)\n"
            )
        )

        env_error_message = (
            f"Also, the following error was thrown when trying to read variables from "
            f"{dotenv_filename}:\n{str(error)}"
            if error
            else ""
        )

        self.missing_vars = missing_vars
        self.example_filename = example_filename
        self.dotenv_filename = dotenv_filename
        self.allow_empty_values = allow_empty_values
        self.error = error

        self.message = "\n\n".join(
            filter(None, [error_message, allow_empty_values_message, env_error_message])
        )

        super().__init__(self.message)
