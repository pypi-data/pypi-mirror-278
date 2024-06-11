from __future__ import annotations

from .dotenv_safe import config
from .missing_env_vars_error import MissingEnvVarsError

__all__ = ["config", "MissingEnvVarsError"]

__version__ = "1.0.0"
