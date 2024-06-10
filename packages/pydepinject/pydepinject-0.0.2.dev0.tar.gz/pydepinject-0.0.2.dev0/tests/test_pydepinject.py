from __future__ import annotations

import functools

import pytest

from pydepinject import requires  # noqa: E402


@pytest.fixture
def venv_root(tmp_path):
    """Return the root directory for virtual environments."""
    path = tmp_path / "venvs"
    path.mkdir()
    return path


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_decorator(venv_root, ephemeral, backend):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    requires_ = functools.partial(
        requires, venv_root=venv_root, ephemeral=ephemeral, venv_backend=backend
    )

    @requires_("six")
    def examplefn():
        print("examplefn")
        import six

        assert six.__version__

    examplefn()
    with pytest.raises(ImportError):
        import six

    if ephemeral:
        assert not list(venv_root.iterdir())
    else:
        assert len(list(venv_root.iterdir())) == 1


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_venv_name_predefined(venv_root, ephemeral, backend):
    assert not list(venv_root.iterdir())

    venv_name = "test_venv_name_predefined"
    with pytest.raises(ImportError):
        import six

    requires_ = functools.partial(
        requires,
        venv_root=venv_root,
        venv_name=venv_name,
        ephemeral=ephemeral,
        venv_backend=backend,
    )

    @requires_("six")
    def examplefn():
        print("examplefn")
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    examplefn()
    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)

    with requires_("six"):
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_venv_name_predefined_env(venv_root, monkeypatch, ephemeral, backend):
    assert not list(venv_root.iterdir())

    venv_name = "test_venv_name_predefined_env"
    monkeypatch.setenv("PYDEPINJECT_VENV_NAME", venv_name)

    with pytest.raises(ImportError):
        import six

    requires_ = functools.partial(
        requires, venv_root=venv_root, ephemeral=ephemeral, venv_backend=backend
    )

    @requires_("six")
    def examplefn():
        print("examplefn")
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    examplefn()
    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)

    with requires_("six"):
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_context_manager(venv_root, ephemeral, backend):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    requires_ = functools.partial(
        requires, venv_root=venv_root, ephemeral=ephemeral, venv_backend=backend
    )
    with requires_("six"):
        import six

        assert six.__version__

    with pytest.raises(ImportError):
        import six

    if ephemeral:
        assert not list(venv_root.iterdir())
    else:
        assert len(list(venv_root.iterdir())) == 1


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
def test_function_call(venv_root, backend):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    requires_instance = requires("six", venv_root=venv_root, venv_backend=backend)
    requires_instance()
    import six

    assert six.__version__
    assert len(list(venv_root.iterdir())) == 1

    requires_instance._deactivate_venv()
    with pytest.raises(ImportError):
        import six
    assert len(list(venv_root.iterdir())) == 1


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
def test_no_installs(venv_root, backend):
    assert not list(venv_root.iterdir())

    @requires("pytest", venv_root=venv_root, ephemeral=False, venv_backend=backend)
    def examplefn():
        print("examplefn")

    examplefn()
    assert not list(venv_root.iterdir())


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
def test_reuse_venv(venv_root, backend):
    assert not list(venv_root.iterdir())

    requires_ = functools.partial(
        requires, venv_root=venv_root, ephemeral=False, venv_backend=backend
    )

    @requires_("six")
    def examplea():
        import six

        assert six.__version__
        examplea.called = True

    @requires_("six")
    def exampleb():
        import six

        assert six.__version__
        global exampleb_called
        exampleb.called = True

    examplea()
    with pytest.raises(ImportError):
        import six

    exampleb()
    with pytest.raises(ImportError):
        import six

    assert examplea.called is exampleb.called is True
    assert len(list(venv_root.iterdir())) == 1


@pytest.mark.parametrize("backend", ["uv", "venv"], ids=["uv", "venv"])
def test_one_venv_multiple_packages(venv_root, backend):
    assert not list(venv_root.iterdir())

    venv_name = "test_one_venv_multiple_packages"

    requires_ = functools.partial(
        requires,
        venv_root=venv_root,
        venv_name=venv_name,
        ephemeral=False,
        venv_backend=backend,
    )

    @requires_("six")
    def examplefn():
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    @requires_("pyparsing")
    def examplefn2():
        import pyparsing

        assert pyparsing.__version__

        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    examplefn()
    examplefn2()

    # Still exists as ephemeral is False.
    assert (venv_root / venv_name).exists()

    with pytest.raises(ImportError):
        import six
    with pytest.raises(ImportError):
        import pyparsing

    assert len(list(venv_root.iterdir())) == 1
