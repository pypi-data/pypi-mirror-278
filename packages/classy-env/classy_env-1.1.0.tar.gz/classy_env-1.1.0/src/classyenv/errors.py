from typing import Any


class ClassyEnvError(Exception):
    """Base Classy Env exception"""


class ClassyEnvClassInstantiatedError(ClassyEnvError):
    def __init__(self) -> None:
        message = "The 'ClassyEnv' class is designed to be subclassed and cannot be instantiated directly."
        super().__init__(message)


class EnvVarNameTypeError(ClassyEnvError, ValueError):
    def __init__(self, envvar_name: Any) -> None:
        message = f"Invalid type: {type(envvar_name)}, expected type: 'str'"
        super().__init__(message)


class EnvVarNameEmptyError(ClassyEnvError, ValueError):
    def __init__(self) -> None:
        message = "Invalid environment variable name: empty string"
        super().__init__(message)


class AttributeMutabilityError(ClassyEnvError, AttributeError):
    def __init__(self, attr_name: str) -> None:
        message = f"Cannot change the value of the {attr_name!r} attribute"
        super().__init__(message)


class EnvVarNotFoundError(ClassyEnvError, ValueError):
    def __init__(self, envvar_name: str) -> None:
        message = f"Couldn't find the {envvar_name!r} environment variable"
        super().__init__(message)


class EnvVarsNotFoundError(ClassyEnvError, ValueError):
    def __init__(self, missing_envvars: list[str]) -> None:
        message = "Couldn't find the following environment variables:\n"
        message += "\n".join(f"\t{envvar!r}" for envvar in missing_envvars)
        super().__init__(message)


class RepeatedEnvVarsError(ClassyEnvError, ValueError):
    def __init__(self, repeated_envvars: list[str]) -> None:
        message = "The following environment variables were declared more than once:\n"
        message += "\n".join(f"\t{envvar!r}" for envvar in repeated_envvars)
        super().__init__(message)
