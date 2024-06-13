import argparse
import functools
import re
from typing import Iterable

from annotated_types import T

from .common import ConfigProperty, always_property


def to_args_key(key: str):
    """Change key to argparse format.

    field_name_of_one_class -> field-name-of-one-class
    fieldNameOfOneClass -> field-name-of-one-class
    FieldNameOfOneClass -> field-name-of-one-class"""
    s1 = re.sub(
        "(_|-)+", "-", key
    )  # replace underscores or multiple hyphens with a single hyphen
    s2 = re.sub(
        "(.)([A-Z][a-z]+)", r"\1-\2", s1
    )  # insert hyphen between lowercase and uppercase
    return re.sub(
        "([a-z0-9])([A-Z])", r"\1-\2", s2
    ).lower()  # insert hyphen between digit/lowercase and uppercase


def to_attr(text: str) -> str:
    """Change flag text to attribute name.

    `--config` -> `config`
    `-c` -> `c`
    `dot-env` -> `dot_env`"""
    while text.startswith("-"):
        text = text[1:]

    text = text.replace("-", "_")
    return text


class BaseArgsConfig:
    """The Base class for config with argparse."""

    parsed_args: argparse.Namespace | None

    def __init__(self):
        self.parsed_args = None

    def load_args(self, parsed_args: argparse.Namespace):
        self.parsed_args = parsed_args


class ArgsConfigProvider:
    parser: argparse.ArgumentParser

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            *args, conflict_handler="resolve", **kwargs
        )

    def from_flag(
        self,
        *use_name_or_flags: str,
        **kwargs,
    ):
        """Config property parse value from argparse flag.

        If no this flag, use the inner value.
        This decorator should be used on the class inherited from BaseArgsConfig.
        Should first parse args, or will not work.

        The args of this decorator is exactly the same as `argparse.ArgumentParser.add_argument`.
        Except the name_or_flags could be optional. If not provided, will use the property name as flag.
        """

        @always_property
        def decorator(prop: ConfigProperty[T]):
            # if provided, use the provided name_or_flags,
            name_or_flags = use_name_or_flags
            if not name_or_flags:
                # else use the function name
                flag = to_args_key(prop.func.__name__)
                name_or_flags = (f"--{flag}",)

            self.parser.add_argument(*name_or_flags, **kwargs)

            if "dest" in kwargs:
                attr_name: str = kwargs["dest"]
            else:
                attr_name = self._parsed_arg_attrs(name_or_flags)

            @functools.wraps(prop.func)
            def impl(innerself: BaseArgsConfig, *args, **kwargs) -> T:
                if not innerself.parsed_args or not attr_name:
                    return prop.func(innerself, *args, **kwargs)

                return innerself.parsed_args.__getattribute__(attr_name) or prop.func(
                    innerself, *args, **kwargs
                )

            return ConfigProperty(impl)

        return decorator

    def _parsed_arg_attrs(self, name_or_flags: Iterable[str]) -> str | None:
        """Get the valid attribute name from the name_or_flags.

        `("-c", "--config")` -> `config`"""
        for name_or_flag in name_or_flags:
            attr_name = to_attr(name_or_flag)
            if len(attr_name) > 1:
                return attr_name

        return None

    def parse_args(self):
        return self.parser.parse_args()
