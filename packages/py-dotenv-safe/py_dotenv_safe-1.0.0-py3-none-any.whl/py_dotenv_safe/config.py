from __future__ import annotations

import os
import sys
from typing import Any, Dict

from .dotenv_safe import config


def main() -> None:
    """
    Load environment variables and configure the application.

    This function is the main entry point to load environment variables and configure
    the application based on the provided options. Options can be provided via
    environment variables or command-line arguments.

    Raises:
        KeyError: If required environment variables are missing.
        ValueError: If command-line arguments are invalid.
        Exception: If an error occurs during configuration.
    """
    options: dict[str, Any] = {}

    # Check for environment variable configuration
    if "DOTENV_CONFIG_EXAMPLE" in os.environ:
        options["examplePath"] = os.environ["DOTENV_CONFIG_EXAMPLE"]

    if os.environ.get("DOTENV_CONFIG_ALLOW_EMPTY_VALUES") != "false":
        options["allowEmptyValues"] = True

    # Parse command-line arguments
    for val in sys.argv:
        if val.startswith("dotenv_config_"):
            key, value = val[len("dotenv_config_") :].split("=", 1)
            options[key] = value

    # Load configuration
    try:
        config_result = config(options)
        print("Configuration loaded successfully:")
        print(config_result)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
