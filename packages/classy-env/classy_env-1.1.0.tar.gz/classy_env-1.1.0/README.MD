# Classy Env

![Tests](https://github.com/mateusz-meksula/classy-env/actions/workflows/tests.yaml/badge.svg) [![](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

Classy Env is a lightweight Python package for managing environment variables in an OOP way.

## Requirements

This package requires Python 3.11 or higher.

## Installation

Classy Env is available on PyPI and can be installed by running the following command:

```shell
pip install classy-env
```

## Usage

Create a `ClassyEnv` subclass and declare its attributes using the `EnvVar` function:

```python
from classyenv import ClassyEnv, EnvVar

class Settings(ClassyEnv):
    database_user = EnvVar("DB_USER")
    database_password = EnvVar("DB_PASSWORD")
    api_secret_key = EnvVar("SECRET_KEY")
```

The `EnvVar` function takes the name of the environment variable as an argument.
The Value of that variable will be assigned to the corresponding attribute.

Then, create an object of your subclass and access the environment variables
through the object's attributes:

```python
settings = Settings()

database_connection = connect(
    user=settings.database_user,
    password=settings.database_password,
)
```

At the object's creation, Classy Env will check if the environment variables
provided to the `EnvVar` functions are defined. If not, an exception will be raised.

This validation can also be triggered at class creation using the `runtime_check` class argument:

```python
from classyenv import ClassyEnv, EnvVar

class Settings(ClassyEnv, runtime_check=True):
    database_user = EnvVar("DB_USER")
    database_password = EnvVar("DB_PASSWORD")
    api_secret_key = EnvVar("SECRET_KEY")
```

### Mutating the `ClassyEnv` instances and subclasses

At this moment, mutating instances of the `ClassyEnv` class is not supported:

```python
settings.database_user = "Roe_Jogan123" # this will raise an exception
```

Similarly, mutating the class attributes of the `ClassyEnv` subclasses is not supported:

```python
Settings.database_user = "Roe_Jogan123" # this will raise an exception
```

## License

This project is licensed under the terms of the MIT license.
