from __future__ import annotations

import os
from typing import Any, Dict, List

from dotenv import dotenv_values, load_dotenv

from .missing_env_vars_error import MissingEnvVarsError


def difference(arr_a: list[str], arr_b: list[str]) -> list[str]:
    """Return the list of elements in arrA that are not in arrB.

    Args:
        arrA (List[str]): The first list.
        arrB (List[str]): The second list.

    Returns:
        List[str]: The difference between the two lists.
    """
    return [a for a in arr_a if a not in arr_b]


def compact(obj: dict[str, Any]) -> dict[str, Any]:
    """Return a dictionary with all falsy values removed.

    Args:
        obj (Dict[str, Any]): The input dictionary.

    Returns:
        Dict[str, Any]: The compacted dictionary.
    """
    return {k: v for k, v in obj.items() if v}


def config(options: dict[str, Any]) -> dict[str, Any]:
    """Load environment variables from a .env file and ensure they match an example .env file.

    Args:
        options (Dict[str, Any]): Configuration options.
            - dotenvPath (str): Path to the .env file.
            - examplePath (str): Path to the example .env file.
            - allowEmptyValues (bool): Whether to allow empty values.

    Returns:
        Dict[str, Any]: Parsed environment variables and any errors.
            - parsed (Dict[str, str]): Parsed environment variables.
            - required (Dict[str, str]): Required environment variables.
            - error (str): Error message if any.

    Raises:
        FileNotFoundError: If either the .env file or the example .env file is not found.
        py_dotenv_safe.missing_env_vars_error.MissingEnvVarsError: If required environment variables are missing.
    """
    dotenv_path = options.get("dotenvPath", ".env")
    example_path = options.get("examplePath", ".env.example")
    allow_empty_values = options.get("allowEmptyValues", False)

    example_vars = {}

    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            raise FileNotFoundError(f"File not found: {dotenv_path}")
        if os.path.exists(example_path):
            example_vars = dotenv_values(example_path)
        else:
            raise FileNotFoundError(f"File not found: {example_path}")
    except FileNotFoundError as e:
        return {"parsed": {}, "required": {}, "error": str(e)}

    env_dict = dict(os.environ.items())
    process_env = env_dict if allow_empty_values else compact(env_dict)

    missing = difference(list(example_vars.keys()), list(process_env.keys()))

    if missing:
        raise MissingEnvVarsError(
            allow_empty_values, dotenv_path, example_path, missing
        )

    required = {key: os.getenv(key) for key in example_vars}

    result = {
        "parsed": dotenv_values(dotenv_path) if os.path.exists(dotenv_path) else {},
        "required": required,
    }

    return result
