import functools
import json
import re
import tomllib
from typing import Callable

import yaml
from annotated_types import T

from .common import ConfigProperty, always_property


def to_unmarshal_key(key: str):
    """Change key to yaml format.
    which should be lower snake case.

    field_name_of_one_class -> field_name_of_one_class
    fieldNameOfOneClass -> field_name_of_one_class
    FieldNameOfOneClass -> field_name_of_one_class
    FIELD_NAME_OF_ONE_CLASS -> field_name_of_one_class"""
    s1 = re.sub(
        "(.)([A-Z][a-z]+)", r"\1_\2", key
    )  # Insert underscore between lower-upper case transitions
    return re.sub(
        "([a-z0-9])([A-Z])", r"\1_\2", s1
    ).lower()  # Insert underscore between digit/lower-upper case transitions


class BaseUnmarshalConfig:
    """The Base class for config with yaml.

    If load multiple files, the later will override the former."""

    registered_loaders: dict[str, Callable[[str], dict]] = {
        ".json": json.loads,
        ".yaml": yaml.safe_load,
        ".yml": yaml.safe_load,
        ".toml": tomllib.loads,
    }

    _dict: dict = {}

    def load(self, loader: callable, file_path: str):
        if not file_path:
            return
        with open(file=file_path, mode="r") as f:
            self._dict = loader(f.read())

    def load_yaml(self, file_path):
        self.load(yaml.safe_load, file_path)

    def load_json(self, file_path):
        self.load(json.loads, file_path)

    def load_toml(self, file_path):
        self.load(tomllib.loads, file_path)

    def register_loader(self, ext: str, loader: Callable[[str], dict]):
        self.registered_loaders[ext] = loader

    def load_auto(self, file_path: str):
        if not file_path:
            return
        for ext, loader in self.registered_loaders.items():
            if file_path.endswith(ext):
                self.load(loader, file_path)
                return

        # file path provided but no loader found
        raise ValueError("Invalid file extension")

    def load_dict(self, config: dict):
        """Load config from dict.

        Useful for testing."""
        self._dict = config


def from_unmarshal(*use_keys: str):
    """Config property parse value from yaml.

    If no this key in yaml, use the inner value.
    This decorator should be used on the class inherited from BaseYamlConfig.
    Should first load yaml file, or will raise an error."""

    @always_property
    def decorator(prop: ConfigProperty[T]):
        if use_keys:
            key = use_keys
        else:
            key = (to_unmarshal_key(prop.func.__name__),)

        @functools.wraps(prop.func)
        def impl(self: BaseUnmarshalConfig, *args, **kwargs) -> dict | T:
            v = self._dict
            for k in key:
                v = v.get(k) if v else None
            return v or prop.func(self, *args, **kwargs)

        return ConfigProperty(impl)

    return decorator
