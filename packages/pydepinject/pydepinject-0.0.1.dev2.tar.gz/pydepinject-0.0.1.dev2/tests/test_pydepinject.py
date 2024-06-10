from __future__ import annotations

import pytest

from pydepinject import requires  # noqa: E402


@pytest.fixture
def venv_root(tmp_path):
    """Return the root directory for virtual environments."""
    path = tmp_path / "venvs"
    path.mkdir()
    return path


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_decorator(venv_root, ephemeral):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    @requires("six", venv_root=venv_root, ephemeral=ephemeral)
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


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_venv_name_predefined(venv_root, ephemeral):
    assert not list(venv_root.iterdir())

    venv_name = "test_venv_name_predefined"
    with pytest.raises(ImportError):
        import six

    @requires("six", venv_root=venv_root, venv_name=venv_name, ephemeral=ephemeral)
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

    with requires("six", venv_root=venv_root, venv_name=venv_name, ephemeral=ephemeral):
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_venv_name_predefined_env(venv_root, monkeypatch, ephemeral):
    assert not list(venv_root.iterdir())

    venv_name = "test_venv_name_predefined_env"
    monkeypatch.setenv("PYDEPINJECT_VENV_NAME", venv_name)

    with pytest.raises(ImportError):
        import six

    @requires("six", venv_root=venv_root, ephemeral=ephemeral)
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

    with requires("six", venv_root=venv_root, ephemeral=ephemeral):
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    with pytest.raises(ImportError):
        import six

    assert (venv_root / venv_name).exists() is (not ephemeral)
    assert len(list(venv_root.iterdir())) == (1 if not ephemeral else 0)


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_context_manager(venv_root, ephemeral):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    with requires("six", venv_root=venv_root, ephemeral=ephemeral):
        import six

        assert six.__version__

    with pytest.raises(ImportError):
        import six

    if ephemeral:
        assert not list(venv_root.iterdir())
    else:
        assert len(list(venv_root.iterdir())) == 1


def test_function_call(venv_root):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    requires_instance = requires("six", venv_root=venv_root)
    requires_instance()
    import six

    assert six.__version__
    assert len(list(venv_root.iterdir())) == 1

    requires_instance._deactivate_venv()
    with pytest.raises(ImportError):
        import six
    assert len(list(venv_root.iterdir())) == 1


def test_no_installs(venv_root):
    assert not list(venv_root.iterdir())

    @requires("pytest", venv_root=venv_root, ephemeral=False)
    def examplefn():
        print("examplefn")

    examplefn()
    assert not list(venv_root.iterdir())


def test_reuse_venv(venv_root):
    assert not list(venv_root.iterdir())

    @requires("six", venv_root=venv_root, ephemeral=False)
    def examplea():
        import six

        assert six.__version__
        examplea.called = True

    @requires("six", venv_root=venv_root, ephemeral=False)
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


def test_one_venv_multiple_packages(venv_root):
    assert not list(venv_root.iterdir())

    venv_name = "test_one_venv_multiple_packages"

    @requires("six", venv_root=venv_root, venv_name=venv_name, ephemeral=False)
    def examplefn():
        import six

        assert six.__version__
        assert (venv_root / venv_name).exists()

    @requires("pyparsing", venv_root=venv_root, venv_name=venv_name, ephemeral=False)
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
