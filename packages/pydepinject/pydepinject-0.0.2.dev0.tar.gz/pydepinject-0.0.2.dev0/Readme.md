# Requirement Manager

This project provides a `RequirementManager` (`requires` is an alias) class to manage Python package requirements using virtual environments. It can be used as a decorator or context manager to ensure specific packages are installed and available during the execution of a function or code block.

## Features

- Automatically creates and manages virtual environments.
- Checks if the required packages are already installed.
- Installs packages if they are not already available.
- Supports ephemeral virtual environments that are deleted after use.
- Can be used as a decorator or context manager.

## Installation

`pip install pydepinject`


## Usage

### Decorator

To use the `requires` as a decorator, simply decorate your function with the required packages:

```python
from pydepinject import requires


@requires("requests", "numpy")
def my_function():
    import requests
    import numpy as np
    print(requests.__version__)
    print(np.__version__)

my_function()
```

### Context Manager

You can also use the `requires` as a context manager:

```python
from pydepinject import requires


with requires("requests", "numpy"):
    import requests
    import numpy as np
    print(requests.__version__)
    print(np.__version__)
```

### Virtual Environment with specific name

The `requires` can create a virtual environment with a specific name:

```python
@requires("requests", venv_name="myenv")
def my_function():
    import requests
    print(requests.__version__)


with requires("pylint", venv_name="myenv"):
    import pylint
    print(pylint.__version__)
    import requests  # This is also available here because it was installed in the same virtual environment
    print(requests.__version__)


# The virtual environment name can also be set as PYDEPINJECT_VENV_NAME environment variable
import os
os.environ["PYDEPINJECT_VENV_NAME"] = "myenv"

@requires("requests")
def my_function():
    import requests
    print(requests.__version__)


with requires("pylint"):
    import pylint
    print(pylint.__version__)
    import requests  # This is also available here because it was installed in the same virtual environment
    print(requests.__version__)
```



### Reusable Virtual Environments

The `requires` can create named virtual environments and reuse them across multiple functions or code blocks:

```python
@requires("requests", venv_name="myenv", ephemeral=False)
def my_function():
    import requests
    print(requests.__version__)


with requires("pylint", venv_name="myenv", ephemeral=False):
    import pylint
    print(pylint.__version__)
    import requests  # This is also available here because it was installed in the same virtual environment
    print(requests.__version__)
```

### Managing Virtual Environments

The `requires` can automatically delete ephemeral virtual environments after use. This is useful when you want to ensure that the virtual environment is clean and does not persist after the function or code block completes:

```python
@requires("requests", venv_name="myenv", ephemeral=True)
def my_function():
    import requests
    print(requests.__version__)

my_function()
```

## Logging

The `requires` uses the `logging` module to provide debug information. By default, it logs to the console at the DEBUG level. You can adjust the logging configuration as needed.

## Unit Tests

Unit tests are provided to verify the functionality of the `requires`. The tests use `pytest` and cover various scenarios including decorator usage, context manager usage, ephemeral environments, and more.

### Running Tests

To run the unit tests, ensure you have `pytest` installed, and then execute the following command:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
