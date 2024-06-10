import dataclasses
import functools
import inspect
from typing import Any, Callable, Generic, Optional, Type

import dacite
import pydantic
from annotated_types import T


class ConfigProperty(Generic[T]):
    """Property for config class.

    The same as cached_property[T], but no cache.
    """

    func: Callable[..., T]

    def __init__(self, func: Callable[..., T]):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(instance)


def always_property(wrapper: Callable[[ConfigProperty[T]], ConfigProperty[T]]):
    """Helper decorator for wrapper.

    Function with this decorator can always assert receiving arg is a property."""

    @functools.wraps(wrapper)
    def wrapped(prop: ConfigProperty[T] | Callable[[], T]) -> ConfigProperty[T]:
        if inspect.isfunction(prop):
            return wrapper(ConfigProperty(prop))
        return wrapper(prop)

    return wrapped


def it_is(
    typ: Type[T],
    *,
    required: bool = False,
    transformer: Optional[Callable[[Any], T]] = None,
):
    """Config property type is typ.

    Because other config source do not consider the type of the value.
    So we need to convert it to the type we want.
    Mostly used on the top of the property."""

    @always_property
    def wrapper(prop: ConfigProperty[T]) -> ConfigProperty[T]:

        @functools.wraps(prop.func)
        def inner(self, *args, **kwargs):
            value: Any = prop.func(self, *args, **kwargs)
            if value is None and required:
                raise ValueError(f"Property {prop.func.__name__} is required.")

            if transformer is not None:
                # top priority to use transformer
                return transformer(value)

            if value is None:
                # not required value can always return None
                return None

            if issubclass(typ, pydantic.BaseModel):
                return _transformer_pydantic(value, typ)
            if dataclasses.is_dataclass(typ):
                return _transformer_dataclass(value, typ)

            return typ(value)

        return ConfigProperty(inner)

    return wrapper


def _transformer_pydantic(value: Any, typ: Type[pydantic.BaseModel]):
    return typ.model_validate(value)


def _transformer_dataclass(value: Any, typ: type):
    assert dataclasses.is_dataclass(typ)
    return dacite.from_dict(typ, value)


def default(default_value: T):
    """Config property default to default_value if no inner value."""

    @always_property
    def wrapper(prop: ConfigProperty[T | None]):

        @functools.wraps(prop.func)
        def inner(self, *args, **kwargs) -> T:
            return prop.func(self, *args, **kwargs) or default_value

        return ConfigProperty(inner)

    return wrapper
