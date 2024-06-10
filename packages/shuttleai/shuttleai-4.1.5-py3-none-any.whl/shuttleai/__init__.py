__title__ = "shuttleai"
__version__ = "4.1.5"

import requests
from packaging import version

from ._patch import _patch_httpx
from .client import AsyncShuttleAI, ShuttleAI


def check_for_updates() -> None:
    try:
        response = requests.get("https://pypi.org/pypi/shuttleai/json")
        latest_version = response.json()["info"]["version"]

        if version.parse(__version__) < version.parse(latest_version):
            print(f"WARNING: You are using an outdated version of {__title__} ({__version__}). "
                  f"The latest version is {latest_version}. It is recommended to upgrade using:\n"
                  f"pip install -U {__title__}")
    except Exception as e:
        print(f"Could not check for updates: {e}")

_patch_httpx()
check_for_updates()

__all__ = ["ShuttleAI", "AsyncShuttleAI"]
