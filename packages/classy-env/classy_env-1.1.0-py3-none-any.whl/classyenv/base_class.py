import os
from typing import Any, Self

from .descriptor import _EnvVar
from .errors import (
    AttributeMutabilityError,
    ClassyEnvClassInstantiatedError,
    EnvVarsNotFoundError,
    RepeatedEnvVarsError,
)


class ClassyEnvMeta(type):
    def __setattr__(cls, name: str, value: Any) -> None:
        for attr_name, attr in cls.__dict__.items():
            if isinstance(attr, _EnvVar) and attr_name == name:
                raise AttributeMutabilityError(attr_name)

        return super().__setattr__(name, value)


class ClassyEnv(metaclass=ClassyEnvMeta):
    """
    Base class for declaring environment variables as class attributes.

    Attributes can be declared as class variables using `EnvVar` function,
    and their values will be automatically fetched from environment variables.

    Example:
    ```python
    class Settings(ClassyEnv):
        secret_key = EnvVar("SECRET_KEY")
        database_host = EnvVar("DB_HOST")

    settings = Settings()
    ```

    """

    def __init_subclass__(cls, runtime_check: bool | None = None) -> None:
        if runtime_check:
            cls._validate()

    def __new__(cls) -> Self:
        if cls is ClassyEnv:
            raise ClassyEnvClassInstantiatedError

        cls._validate()

        return super().__new__(cls)

    @classmethod
    def _validate(cls) -> None:
        if getattr(cls, "is_validated", False):
            return

        declared_envvars = []
        missing_envvars = []
        repeated_envvars = []

        for attr in cls.__dict__.values():
            if isinstance(attr, _EnvVar):
                try:
                    os.environ[attr.envvar_name]
                except KeyError:
                    if attr.envvar_name not in missing_envvars:
                        missing_envvars.append(attr.envvar_name)

                if (
                    attr.envvar_name in declared_envvars
                    and attr.envvar_name not in repeated_envvars
                ):
                    repeated_envvars.append(attr.envvar_name)
                declared_envvars.append(attr.envvar_name)

        if repeated_envvars and missing_envvars:
            raise ExceptionGroup(
                f"The following errors occurred while trying to instantiate object of the {cls.__name__!r} class:",
                [
                    RepeatedEnvVarsError(repeated_envvars),
                    EnvVarsNotFoundError(missing_envvars),
                ],
            )

        if repeated_envvars:
            raise RepeatedEnvVarsError(repeated_envvars)

        if missing_envvars:
            raise EnvVarsNotFoundError(missing_envvars)

        cls.is_validated = True
