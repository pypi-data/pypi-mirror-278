from __future__ import annotations

import functools
import hashlib
import logging
import os
import pathlib
import shutil
import sys
import tempfile
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType
    from typing import Any
    from .backends import VenvBackend

from .backends import VenvBackendRegistry

VERSION = "0.0.2dev0"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

VENV_ROOT = pathlib.Path(
    os.environ.get("PYDEPINJECT_VENV_ROOT", None)
    or pathlib.Path(tempfile.gettempdir()) / __name__.split(".")[0] / "venvs"
)
logger.debug("VENV_ROOT: %s", VENV_ROOT)

VENV_BACKENDS = "|".join(VenvBackendRegistry.get_backends())
logger.debug("VENV_BACKENDS: %s", VENV_BACKENDS)


def is_requirements_satisfied(*packages: str):
    """Check if the requirements are already satisfied. Return None if it cannot be determined."""
    try:
        from importlib.metadata import PackageNotFoundError, distribution

        from packaging.requirements import Requirement
    except ImportError:
        try:
            from importlib.metadata import PackageNotFoundError, distribution

            from packaging.requirements import Requirement
        except ImportError:
            logger.warning(
                "importlib.metadata and packaging not found. Cannot check if requirements are satisfied."
            )
            return None

    try:
        for package in packages:
            logger.debug("Checking package: %s", package)
            req = Requirement(package)
            try:
                dist = distribution(req.name)
                if dist.version not in req.specifier:
                    logger.debug(
                        "Requirement %s is not satisfied. Version conflict.", package
                    )
                    return False
                logger.debug("Requirement %s is satisfied", package)
            except PackageNotFoundError:
                logger.debug(
                    "Requirement %s is not satisfied. Distribution not found.", package
                )
                return False
        return True
    except Exception as e:
        logger.warning("An error occurred while checking requirements: %s", str(e))
        return None


class RequirementManager:
    """A decorator and context manager to manage Python package requirements."""

    def __init__(
        self,
        *packages: str,
        venv_name: str | None = None,
        venv_root: pathlib.Path = VENV_ROOT,
        venv_backend: str | None = None,
        recreate: bool = False,
        ephemeral: bool = False,
    ):
        """Initialize the RequirementManager.

        Args:
            *packages: A list of package requirements.
            venv_name: The name of the virtual environment. If not provided,
                a unique name will be generated based on the package requirements.
            venv_root: The root directory for virtual environments.
            venv_backend: The virtual environment backend to use. Defaults to $PYDEPINJECT_VENV_NAME or "uv|venv".
            recreate: If True, the virtual environment will be recreated if it exists.
            ephemeral: If True, the virtual environment will be deleted after use.
        """
        self.packages = packages
        self.venv_name = venv_name or os.environ.get("PYDEPINJECT_VENV_NAME", "")
        self.original_pythonpath = os.environ.get("PYTHONPATH", "")
        self.original_path = os.environ.get("PATH", "")
        self.original_syspath = sys.path.copy()
        self._venv_path = venv_root / self.venv_name if self.venv_name else None
        self._venv_root = venv_root

        venv_backend = (
            venv_backend
            or os.environ.get("PYDEPINJECT_VENV_BACKEND", None)
            or VENV_BACKENDS
        )
        self._venv_backends = [item.strip() for item in venv_backend.split("|")]
        invalid_backends = set(self._venv_backends) - set(VENV_BACKENDS.split("|"))
        if invalid_backends:
            raise ValueError(f"Invalid venv_backend: {','.join(invalid_backends)}")

        self.ephemeral = ephemeral
        self.recreate = recreate
        self._activated = False

    @property
    def venv_backend_cls(self) -> type[VenvBackend]:
        """Returns the virtual environment backend class."""
        supported_backends = VenvBackendRegistry.get_supported_backends()
        for backend in self._venv_backends:
            if backend not in supported_backends:
                continue
            return supported_backends[backend]
        raise ValueError("No supported venv backend found")

    @property
    def venv_path(self):
        if self._venv_path:
            """Returns a path to the virtual environment. If not set, a unique path is generated."""
            return self._venv_path
        # Create a unique hash for the package requirements
        reqs_str = ",".join(self.packages)
        reqs_hash = hashlib.md5(reqs_str.encode()).hexdigest()

        self._venv_path = self._venv_root / reqs_hash
        return self._venv_path

    def _create_virtualenv(self):
        """Create a virtual environment if it does not exist."""
        if self.venv_path.exists() and not self.recreate:
            return
        logger.debug("Creating virtualenv: %s", self.venv_path)
        self.venv_backend_cls(self.venv_path).create(clear=self.recreate)

    def _install_packages(self):
        logger.info("Installing packages: %s", self.packages)
        self.venv_backend_cls(self.venv_path).install(*self.packages)

    def _activate_venv(self):
        if is_requirements_satisfied(*self.packages):
            logger.debug(
                "Requirements %s already satisfied. No need to create venv",
                self.packages,
            )
            return self

        self.original_pythonpath = os.environ.get("PYTHONPATH", "")
        self.original_path = os.environ.get("PATH", "")
        self.original_syspath = sys.path.copy()

        self._create_virtualenv()

        venv_site_packages = pathlib.Path(self.venv_path).joinpath(
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages",
        )
        os.environ["PYTHONPATH"] = str(venv_site_packages) + (
            os.pathsep + self.original_pythonpath if self.original_pythonpath else ""
        )
        os.environ["PATH"] = (
            str(pathlib.Path(self.venv_path) / "bin") + os.pathsep + self.original_path
        )
        sys.path.insert(0, str(venv_site_packages))
        self._activated = True
        if is_requirements_satisfied(*self.packages):
            logger.debug(
                "Requirements %s already satisfied within %s",
                self.packages,
                self.venv_path,
            )
            return self
        self._install_packages()

    def _deactivate_venv(self):
        if not self._activated:
            return
        os.environ["PATH"] = self.original_path
        os.environ["PYTHONPATH"] = self.original_pythonpath
        sys.path = self.original_syspath
        # Cleanup imported cached modules from the temporary venv.
        venv_imports: set[str] = set()
        for name, module in sys.modules.items():
            module_path = getattr(module, "__file__", None)
            if module_path and pathlib.Path(module_path).is_relative_to(self.venv_path):
                venv_imports.add(name)
        for name in venv_imports:
            del sys.modules[name]
        self._activated = False
        if self.ephemeral:
            logger.debug("Deleting ephemeral venv: %s", self.venv_path)
            shutil.rmtree(self.venv_path)

    def __enter__(self):
        self._activate_venv()
        return self

    def __exit__(
        self,
        exctype: type[BaseException] | None,
        excinst: BaseException | None,
        exctb: TracebackType | None,
    ) -> None:
        del exctype, excinst, exctb
        self._deactivate_venv()

    def __call__(self, func: Callable[..., Any] | None = None):
        if func is None:
            self._activate_venv()
            return

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            with self:
                return func(*args, **kwargs)

        return wrapper


requires = RequirementManager
