import os
import subprocess
import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from snowflake.cli import __about__

TEST_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def test_root_path():
    return TEST_DIR


@pytest.fixture(autouse=True)
def disable_colors_and_styles_in_output(monkeypatch):
    """
    Colors and styles in output cause mismatches in asserts,
    this environment variable turn off styling
    """
    monkeypatch.setenv("TERM", "unknown")


@pytest.fixture
def temp_dir():
    initial_dir = os.getcwd()
    tmp = tempfile.TemporaryDirectory()
    os.chdir(tmp.name)
    yield tmp.name
    os.chdir(initial_dir)
    tmp.cleanup()


@pytest.fixture(scope="session")
def snowcli(test_root_path):
    with TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        _create_venv(tmp_dir_path)
        _build_snowcli(tmp_dir_path, test_root_path)
        _install_snowcli_with_external_plugin(tmp_dir_path, test_root_path)
        yield tmp_dir_path / "bin" / "snow"


@pytest.fixture(autouse=True)
def isolate_default_config_location(monkeypatch, temp_dir):
    monkeypatch.setenv("SNOWFLAKE_HOME", temp_dir)


def _create_venv(tmp_dir: Path) -> None:
    subprocess.check_call(["python", "-m", "venv", tmp_dir])


def _build_snowcli(venv_path: Path, test_root_path: Path) -> None:
    subprocess.check_call(
        [_python_path(venv_path), "-m", "pip", "install", "--upgrade", "build"]
    )
    subprocess.check_call(
        [_python_path(venv_path), "-m", "build", test_root_path / ".."]
    )


def _pip_install(python, *args):
    return subprocess.check_call([python, "-m", "pip", "install", *args])


def _install_snowcli_with_external_plugin(
    venv_path: Path, test_root_path: Path
) -> None:
    version = __about__.VERSION
    python = _python_path(venv_path)
    _pip_install(
        python,
        test_root_path / f"../dist/snowflake_cli_labs-{version}-py3-none-any.whl",
    )
    _pip_install(
        python,
        test_root_path.parent
        / "test_external_plugins"
        / "multilingual_hello_command_group",
    )

    # Required by snowpark example tests
    _pip_install(python, "snowflake-snowpark-python")


def _python_path(venv_path: Path) -> Path:
    return venv_path / "bin" / "python"
