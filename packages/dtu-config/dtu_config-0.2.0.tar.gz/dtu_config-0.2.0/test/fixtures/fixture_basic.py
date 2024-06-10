"""Fixtures for module testing."""
import io

import pytest
from appdirs import user_config_dir

from dtu_config import DTU_config

# =============================================================================
# Example path
# =============================================================================


@pytest.fixture
def path():
    """Return the default path to use in tests."""
    # we may want the path to include authors for windows users
    return f"{user_config_dir()}/pywasp/pywasp.ini"


# =============================================================================
# Example configurations
# =============================================================================


@pytest.fixture
def initial_dtu_config(path):
    """Return an empty configuration object."""
    conf = DTU_config.DtuConfig(path)
    conf.finalise()
    return conf


@pytest.fixture
def example_dtu_config(monkeypatch, path, capsys):
    """Return a configuration with a test int and str."""
    # setup
    monkeypatch.setattr("sys.stdin", io.StringIO("\n\n"))
    conf = DTU_config.DtuConfig(path)
    conf.add_int("test", "integer", default="0")
    conf.add_str("test", "string", default="Test string")
    conf.create_config()
    conf.finalise()
    _, _ = capsys.readouterr()

    yield conf

    # teardown
    conf = DTU_config.DtuConfig(path)
    conf.finalise()


@pytest.fixture
def incomplete_config(monkeypatch, path):
    """Return a configuration with string set, required int not set."""
    # setup
    monkeypatch.setattr("sys.stdin", io.StringIO("\n" * 6))
    conf = DTU_config.DtuConfig(path)
    conf.add_int("test", "integer")
    conf.add_str("test", "string", default="Test string")
    conf.create_config()
    conf.finalise()

    yield conf

    # teardown
    conf = DTU_config.DtuConfig(path)
    conf.finalise()


# =============================================================================
# Example output
# =============================================================================


@pytest.fixture
def example_text():
    """Return example print for example_dtu_config.view()."""
    return """=== SECTIONS ===
DEFAULT <Section: DEFAULT>
test <Section: test>\n\n
=== DEFAULT ===\n
=== test ===
integer 0
string Test string"""


# =============================================================================
# List of methods
# =============================================================================


@pytest.fixture
def conf_and_methods(initial_dtu_config):
    """Return an empty configuration and its add_* method to be tested."""
    return (
        initial_dtu_config,
        [
            initial_dtu_config.add_url,
            initial_dtu_config.add_bool,
            initial_dtu_config.add_str,
            initial_dtu_config.add_int,
        ],
    )


# =============================================================================
# Example inputs
# =============================================================================


@pytest.fixture
def sections():
    """Return a list of str to use as section names."""
    return ["test"] * 6


@pytest.fixture
def keys():
    """Return a list of str to be used as key names."""
    return ["url", "bool", "string", "integer", "email", "phone"]


@pytest.fixture
def defaults():
    """Return a list of default values for the add_* methods."""
    return [
        "https://www.google.com/",
        "True",
        "Testing!",
        "0",
        "wind@domain.com",
        "+4500000000",
    ]


@pytest.fixture
def valid_indexes_and_input():
    """Return list of strings to be used as std input when creating config."""
    return (
        [1, 3, 4, 6, 8, 10],
        [
            "not an url",
            "https://www.google.com/",
            "not a bool",
            "True",
            "Every string works",
            "not an integer",
            "3",
            "not an email",
            "wind@domain.com",
            "not a phone number",
            "+4500000000",
        ],
    )
