import os

import pytest

from classyenv import ClassyEnv, EnvVar, errors

FOO_ENV = "FOO_ENVVAR_VALUE"
BAR_ENV = "BAR_ENVVAR_VALUE"

os.environ["FOO"] = FOO_ENV
os.environ["BAR"] = BAR_ENV


class Settings(ClassyEnv):
    foo = EnvVar("FOO")
    bar = EnvVar("BAR")


class NotPresentSettings(ClassyEnv):
    test_env1 = EnvVar("TEST1")
    test_env2 = EnvVar("TEST2")


class DoubledSettings(ClassyEnv):
    foo = EnvVar("FOO")
    bar = EnvVar("FOO")


class NotPresentAndDoubledSettings(ClassyEnv):
    test_env1 = EnvVar("TEST1")
    test_env2 = EnvVar("TEST2")
    test_env3 = EnvVar("TEST1")
    test_env4 = EnvVar("TEST2")


def test_can_access_envvars_correctly():
    obj = Settings()

    assert obj.foo == FOO_ENV
    assert obj.bar == BAR_ENV


def test_can_access_envvars_as_class_attributes():
    assert Settings.foo == FOO_ENV
    assert Settings.bar == BAR_ENV


def test_cannot_mutate_class_attr():
    with pytest.raises(errors.AttributeMutabilityError) as e:
        Settings.foo = "TEST"

    assert "Cannot change the value of the 'foo' attribute" == e.value.args[0]


def test_cannot_mutate_attr():
    obj = Settings()

    with pytest.raises(errors.AttributeMutabilityError) as e:
        obj.foo = "TEST"

    assert "Cannot change the value of the 'foo' attribute" == e.value.args[0]


def test_cannot_pass_non_string_envvar_name():
    with pytest.raises(errors.EnvVarNameTypeError) as e:
        EnvVar(123)  # type: ignore

    assert "Invalid type: <class 'int'>, expected type: 'str'" == e.value.args[0]


def test_cannot_pass_empty_string_envvar_name():
    with pytest.raises(errors.EnvVarNameEmptyError) as e:
        EnvVar("")

    assert "Invalid environment variable name: empty string" == e.value.args[0]


def test_raises_error_when_instantiates_invalid_class():
    with pytest.raises(errors.EnvVarsNotFoundError) as e:
        NotPresentSettings()

    assert (
        "Couldn't find the following environment variables:\n\t'TEST1'\n\t'TEST2'"
        == e.value.args[0]
    )


def test_raises_error_when_accessing_invalid_class_attribute():
    with pytest.raises(errors.EnvVarNotFoundError) as e:
        NotPresentSettings.test_env1

    assert "Couldn't find the 'TEST1' environment variable" == e.value.args[0]


def test_cannot_instantiate_settings_with_doubled_envvars():
    with pytest.raises(errors.RepeatedEnvVarsError) as e:
        DoubledSettings()

    assert (
        "The following environment variables were declared more than once:\n\t'FOO'"
        == e.value.args[0]
    )


def test_raises_exception_group_when_there_are_two_errors():
    with pytest.raises(ExceptionGroup) as e:
        NotPresentAndDoubledSettings()

    assert (
        "The following errors occurred while trying to instantiate object of the 'NotPresentAndDoubledSettings' class:"
        == e.value.args[0]
    )


def test_cannot_instantiate_classy_env_class():
    with pytest.raises(errors.ClassyEnvClassInstantiatedError) as e:
        ClassyEnv()

    assert (
        "The 'ClassyEnv' class is designed to be subclassed and cannot be instantiated directly."
        == e.value.args[0]
    )


def test_runtime_validation_env_vars_not_defined():
    with pytest.raises(errors.EnvVarsNotFoundError) as e:

        class NotPresentSettings(ClassyEnv, runtime_check=True):
            test_env1 = EnvVar("TEST1")
            test_env2 = EnvVar("TEST2")

    assert (
        "Couldn't find the following environment variables:\n\t'TEST1'\n\t'TEST2'"
        == e.value.args[0]
    )


def test_runtime_validation_repeated_env_vars():
    with pytest.raises(errors.RepeatedEnvVarsError) as e:

        class DoubledSettings(ClassyEnv, runtime_check=True):
            foo = EnvVar("FOO")
            bar = EnvVar("FOO")

    assert (
        "The following environment variables were declared more than once:\n\t'FOO'"
        == e.value.args[0]
    )


def test_runtime_validation_env_vars_not_defined_and_repeated_env_vars():
    with pytest.raises(ExceptionGroup) as e:

        class NotPresentAndDoubledSettings(ClassyEnv, runtime_check=True):
            test_env1 = EnvVar("TEST1")
            test_env2 = EnvVar("TEST2")
            test_env3 = EnvVar("TEST1")
            test_env4 = EnvVar("TEST2")

    assert (
        "The following errors occurred while trying to instantiate object of the 'NotPresentAndDoubledSettings' class:"
        == e.value.args[0]
    )
