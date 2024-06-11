"""Configuration file for the whole antconnect v2 python package.
"""

import inspect
from urlpath import URL
from pathlib import Path


model_base_class_name = "ModelBaseClass"
empty_default = inspect._empty


class HostUrlConfig:
    host: URL = URL("https://api.alpha.antcde.io")  # "https://api.antcde.io/"
    data_model: URL = URL("https://api-alpha.antcde.io/docs/2.0/api-docs-v2.json")
    type: str = "api"
    version: str = "2.0"
    documentation: URL = URL("https://api-alpha.antcde.io/api/2.0/documentation")


class TokenConfig:
    endpoint: URL = URL("oauth/token")


class RequestsConfig:
    verify: bool = True
    headers: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "access_token_placeholder",
    }
    _placeholder_string: str = "Bearer {}"


class ThrottleConfig:
    amount: int = 120
    time_frame: int = 60


class Directories:
    ROOT: Path = Path(__file__).parent.parent.parent
    DEV: Path = ROOT / "dev"
    TEST_DOCS: Path = DEV / "testing"
    PROJECT_SRC: Path = ROOT / "src" / "ant_connect"


class ProjectPaths:
    MODELS: Path = Directories.PROJECT_SRC / "models.py"
    LOCAL_DATA_MODEL: Path = Directories.DEV / "testing" / "api-docs-v2.11.json"
    MANUAL_FUNCTIONS: Path = Directories.PROJECT_SRC / "utils" / "manual_functions.py"