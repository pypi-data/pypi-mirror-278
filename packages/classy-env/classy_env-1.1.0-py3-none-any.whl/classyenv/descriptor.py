import os
from typing import Any, Literal, NoReturn, overload

from .errors import (
    AttributeMutabilityError,
    EnvVarNameEmptyError,
    EnvVarNameTypeError,
    EnvVarNotFoundError,
)


class _EnvVar:
    def __init__(self, envvar_name: str) -> None:
        self.envvar_name = envvar_name

    def __set_name__(self, owner, name) -> None:
        self.attr_name = name

    def __get__(self, obj, obj_type=None):
        try:
            return os.environ[self.envvar_name]
        except KeyError:
            raise EnvVarNotFoundError(self.envvar_name)

    def __set__(self, obj, value: str):
        raise AttributeMutabilityError(self.attr_name)


@overload
def EnvVar(envvar_name: Literal[""]) -> NoReturn: ...
@overload
def EnvVar(envvar_name: str) -> Any: ...


def EnvVar(envvar_name):
    """
    Function intended to be used as a default value for class
    attributes in classes that inherit from `ClassyEnv` class.

    When used, it validates the value of `envvar_name` parameter and returns the `_EnvVar` descriptor.

    Example:
    ```python
    from classyenv import ClassyEnv, EnvVar

    class Settings(ClassyEnv):
        path = EnvVar("PATH")
    ```
    """

    if not isinstance(envvar_name, str):
        raise EnvVarNameTypeError(envvar_name)

    if envvar_name == "":
        raise EnvVarNameEmptyError

    return _EnvVar(envvar_name)
