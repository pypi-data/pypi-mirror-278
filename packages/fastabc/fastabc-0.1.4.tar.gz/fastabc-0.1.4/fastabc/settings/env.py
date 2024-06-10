import os
from typing import Sequence

from dotenv import load_dotenv

from fastabc.exceptions import EnvironmentNotFound


def load_env(
    env_files: Sequence[str] = (".dev.env", ".prod.env", ".env"),
    no_env_file_var: str = "NO_ENV_FILE",
) -> bool:
    if os.getenv(no_env_file_var):
        return False
    for file in env_files:
        if load_dotenv(file):
            return True
    raise EnvironmentNotFound(f"Environment file not found: {env_files}")
