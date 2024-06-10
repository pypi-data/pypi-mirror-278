from __future__ import annotations

import collections
import logging
import pathlib
import shutil
import subprocess
import sys
import typing
from typing import Protocol

if typing.TYPE_CHECKING:
    from collections.abc import MutableMapping

_PYTHON_BIN = sys.executable

logger = logging.getLogger(__name__)


class VenvBackend(Protocol):
    """Protocol for virtual environment backends."""

    _path: pathlib.Path
    _PRIORITY: int

    def __init__(self, path: str | pathlib.Path): ...

    @property
    def name(self) -> str: ...

    def create(self, clear: bool = False) -> None: ...

    def install(self, *packages: str) -> None: ...

    @classmethod
    def is_supported(cls) -> bool: ...


class VenvBackendRegistry:
    """Registry of virtual environment backends."""

    _registry: MutableMapping[str, type[VenvBackend]] = {}

    @classmethod
    def register_backend(cls, backend_cls: type[VenvBackend]) -> None:
        instance = backend_cls(
            pathlib.Path()
        )  # Create an instance to access the name property
        cls._registry[instance.name] = backend_cls

    @classmethod
    def get_backend(cls, name: str) -> type[VenvBackend] | None:
        return cls._registry.get(name)

    @classmethod
    def has_backend(cls, name: str) -> bool:
        return name in cls._registry

    @classmethod
    def get_backends(cls) -> MutableMapping[str, type[VenvBackend]]:
        result: MutableMapping[str, type[VenvBackend]] = collections.OrderedDict()
        for name in sorted(cls._registry, key=lambda x: cls._registry[x]._PRIORITY):  # pyright: ignore[reportPrivateUsage]
            result[name] = cls._registry[name]
        return result

    @classmethod
    def get_supported_backends(cls) -> dict[str, type[VenvBackend]]:
        return {
            name: backend_cls
            for name, backend_cls in cls._registry.items()
            if backend_cls.is_supported()
        }


class VenvBackendVenv:
    """Virtual environment backend using the venv module."""

    _NAME = "venv"
    _PRIORITY: int = 0

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)

    @property
    def name(self) -> str:
        return self._NAME

    @classmethod
    def is_supported(cls) -> bool:
        return True

    def create(self, clear: bool = False) -> None:
        clear_opt = ["--clear"] if clear else []
        venv_args = [_PYTHON_BIN, "-m", "venv"] + clear_opt + [str(self._path)]
        logger.debug("Running command: %s", " ".join(venv_args))
        subprocess.check_call(venv_args)

    def install(self, *packages: str) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"Virtual environment not found: {self._path}")

        pip_executable = self._path / "bin" / "pip"
        if not pip_executable.exists():
            raise FileNotFoundError(f"pip executable not found: {pip_executable}")

        pip_args = [
            str(pip_executable),
            "install",
            "--quiet",
            "--no-python-version-warning",
            "--disable-pip-version-check",
            "--upgrade",
            *packages,
        ]
        logger.debug("Running command: %s", " ".join(pip_args))
        subprocess.check_call(pip_args)


class VenvBackendUV:
    """Virtual environment backend using the uv tool."""

    _NAME = "uv"
    _PRIORITY: int = 1
    _CMD = "uv"

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)

    @property
    def name(self) -> str:
        return self._NAME

    @classmethod
    def is_supported(cls) -> bool:
        return bool(shutil.which(cls._CMD))

    def create(self, clear: bool = False) -> None:
        if clear and self._path.exists():
            shutil.rmtree(self._path)
        subprocess.check_call([
            f"{self._CMD}",
            "venv",
            "--python",
            _PYTHON_BIN,
            self._path.as_posix(),
        ])

    def install(self, *packages: str) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"Virtual environment not found: {self._path}")
        pip_args = [
            f"{self._CMD}",
            "pip",
            "install",
            "--python",
            (self._path / "bin" / "python").as_posix(),
            "--quiet",
            "--upgrade",
            *packages,
        ]
        logger.debug("Running command: %s", " ".join(pip_args))
        subprocess.check_call(pip_args)


# Register backends
VenvBackendRegistry.register_backend(VenvBackendVenv)
VenvBackendRegistry.register_backend(VenvBackendUV)
