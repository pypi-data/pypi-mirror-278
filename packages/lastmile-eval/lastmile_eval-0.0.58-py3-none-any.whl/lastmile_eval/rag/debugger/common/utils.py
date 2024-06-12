"""
Utils file for various needs in the RAG debugger.
"""

import requests
from requests import Response
import os
from typing import Optional

import dotenv

SHOW_DEBUG = False
LASTMILE_SPAN_KIND_KEY_NAME = "lastmile.span.kind"


class Singleton:
    """
    Define a Singleton object that we can extend to create singleton classes.
    This is needed/helpful for ensuring trace-level data is the same when used
    across multiple classes. An alternative to using a singleton is ensuring
    that a shared state object is passed around correctly to all callsites

    This implementation is what's found on the Python docs:
    https://www.python.org/download/releases/2.2/descrintro/#__new__
    Please note that it is not thread-safe
    """

    def __new__(cls, *args, **kwargs):  # type: ignore[errggh *pukes*]
        it = cls.__dict__.get("__it__")  # dude
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)  # type: ignore[im going to pretend i didnt see that *pukes*]
        return it

    def init(self, *args, **kwargs):  # type: ignore[mate]
        """
        Sets the _is_already_initialized flag to True. Use this in your
        cubslass with the following implementation

        class MySingleton(Singleton):
            _is_already_initialized = False

            def __init__(self):
                if self._is_already_initialized:
                    return
                super().__init__()
                # Other logic here to initialize singleton once
                ...
                _is_already_initialized = False
        """


def get_lastmile_api_token(lastmile_api_token: Optional[str] = None) -> str:
    """
    Helper function to get the LastMile API token. If the lastmile_api_token
    is None, then we try to get the token from the environment variables. If
    the token is still None, then we raise a ValueError.

    @param lastmile_api_token Optional(str): The LastMile API token to use.
        If None, then we try to get the token from the environment variables

    @return str: The LastMile API token to use
    """
    if lastmile_api_token is None:
        dotenv.load_dotenv()
        lastmile_api_token = os.getenv("LASTMILE_API_TOKEN")
        if lastmile_api_token is None:
            raise ValueError(
                "Cannot find `lastmile_api_token`. Please create one from the 'API Tokens' section from this website: https://lastmileai.dev/settings?page=tokens"
            )
    return lastmile_api_token


def raise_for_status(response: Response, message: str) -> None:
    """
    Raise an HTTPError exception if the response is not successful
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(f"{message}: {response.content}") from e
