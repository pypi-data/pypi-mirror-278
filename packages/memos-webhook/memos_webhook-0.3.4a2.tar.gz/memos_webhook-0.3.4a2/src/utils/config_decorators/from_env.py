import functools
import os
import re
from typing import IO, Optional

import dotenv
from annotated_types import T

from .common import ConfigProperty, always_property


def to_env_key(key: str):
    """Change key to environment variable format,
    which should be upper snake case.

    field_name_of_one_class -> FIELD_NAME_OF_ONE_CLASS
    fieldNameOfOneClass -> FIELD_NAME_OF_ONE_CLASS
    FieldNameOfOneClass -> FIELD_NAME_OF_ONE_CLASS"""
    s1 = re.sub(
        "(.)([A-Z][a-z]+)", r"\1_\2", key
    )  # Insert underscore between lower-upper case transitions
    return re.sub(
        "([a-z0-9])([A-Z])", r"\1_\2", s1
    ).upper()  # Insert underscore between digit/lower-upper case transitions


def from_env(use_key: str | None = None):
    """Config property parse value from environment variable.

    If no this environment variable, use the inner value."""

    @always_property
    def decorator(prop: ConfigProperty[T]):
        if use_key:
            key = use_key
        else:
            key = to_env_key(prop.func.__name__)

        @functools.wraps(prop.func)
        def impl(self, *args, **kwargs):
            return os.environ.get(key) or prop.func(self, *args, **kwargs)

        return ConfigProperty(impl)

    return decorator


class BaseDotenvConfig:
    """The Base class for config with dotenv.

    All parameters are same as dotenv.load_dotenv."""

    def load_dotenv(
        self,
        dotenv_path: Optional[str] = None,
        stream: Optional[IO[str]] = None,
        verbose: bool = False,
        override: bool = False,
        interpolate: bool = True,
        encoding: Optional[str] = "utf-8",
    ):
        dotenv.load_dotenv(
            dotenv_path,
            stream,
            verbose,
            override,
            interpolate,
            encoding,
        )
