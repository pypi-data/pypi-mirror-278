"""Tests for DTU_Config basic features."""

# import importlib
import io

import phonenumbers
import pytest

from dtu_config import DTU_config

# =============================================================================
# Test add methods
# =============================================================================


def test_add_default(monkeypatch, conf_and_methods, sections, keys, defaults):
    """add_int + default create config.

    Parameters
    ----------
    methods : list of methods
    sections, keys: lists of str
        sections, keys to be used as paramters in the respective methods
    input_ : str
        Concatenated inputs to be used in respective methods. Each input should
        end with an end of line.
    defaults: list of different types(str, bool, int)
        default values to be used as paramters in the respective methods

    """
    # get configuration, ethods and std input
    conf, methods = conf_and_methods
    monkeypatch.setattr("sys.stdin", io.StringIO("\n".join(defaults)))

    # use methods
    for i, function in enumerate(methods):
        function(sections[i], keys[i], default=defaults[i])
    conf.create_config()

    # test that configuration got the required elements
    for i in range(len(methods)):
        assert conf._config.has_option(sections[i], keys[i])
        assert conf._config[sections[i]][keys[i]] == defaults[i]


def test_add(monkeypatch, conf_and_methods, sections, keys, valid_indexes_and_input):
    """add_int + create config with appropriate and inappropriate input.

    create_config should repeat prompt when an inappropriate input is used.

    Parameters
    ----------
    methods : list of methods
    sections, keys: lists of str
        sections, keys to be used as paramters in the respective methods
    input_ : str
        Concatenated inputs to be used in respective methods. Each input should
        end with an end of line.
    input_: list of different types(str, bool, int)
        default values to be used as paramters in the respective methods

    """
    # get configuration, ethods and std input
    conf, methods = conf_and_methods
    valid, input_ = valid_indexes_and_input
    monkeypatch.setattr("sys.stdin", io.StringIO("\n".join(input_)))

    # use methods
    for i, function in enumerate(methods):
        function(sections[i], keys[i])
    conf.create_config()

    # test that configuration got the required elements
    for i in range(len(methods)):
        assert conf._config.has_option(sections[i], keys[i])
        assert conf._config[sections[i]][keys[i]] == input_[valid[i]]


# =============================================================================
# Test command line tool
# =============================================================================


def test_cmd(
    example_dtu_config, sections, keys, valid_indexes_and_input, capsys, monkeypatch
):
    """Test command line for invalid and valid input"""
    # setup
    valid, input_ = valid_indexes_and_input
    i = 3
    monkeypatch.setattr("sys.stdin", io.StringIO("5"))
    _, _ = capsys.readouterr()  # ignore setup output

    # invalid input
    example_dtu_config.cmd_tool(
        args=[f"--set-{sections[i]}-{keys[i]}", input_[valid[i] - 1]]
    )
    out, err = capsys.readouterr()
    assert out.strip().split("\n")[-1] == "Please enter integer [default: 0]"

    # correction
    assert example_dtu_config._config[sections[i]][keys[i]] == "5"

    # another valid input
    example_dtu_config.cmd_tool(
        args=[f"--set-{sections[i]}-{keys[i]}", input_[valid[i]]]
    )
    assert example_dtu_config._config[sections[i]][keys[i]] == input_[valid[i]]


def test_cmd_warning(incomplete_config, recwarn):
    """Check that the command line throws an error when using non complete config"""
    incomplete_config.cmd_tool(args=["--set-test-string", "wind"])
    assert len(recwarn) == 1
    w = recwarn.pop()
    assert str(w.message) == "Option integer of section test is required and not set."


# =============================================================================
# Test valid phone numbers
# =============================================================================


def test_valid_phonenumber():
    assert DTU_config.is_valid_phone_number("+1 650-253-0000")


def test_invalid_phonenumber():
    with pytest.raises(phonenumbers.NumberParseException) as exc_info:
        DTU_config.is_valid_phone_number("650-253-0000")
        assert str(exc_info.value) == "(0) Missing or invalid default region."


# =============================================================================
# Other tests
# =============================================================================


def test_str(example_dtu_config, example_text, capsys):
    """view method should print the sections, options, values."""
    # ignore setup output
    _, _ = capsys.readouterr()
    # print configuration and check std out
    print(example_dtu_config)
    out, err = capsys.readouterr()
    assert out.strip() == example_text


def test_get(incomplete_config, example_dtu_config, capsys, recwarn):
    incomplete_config.get_option("test", "integer")
    out, err = capsys.readouterr()
    assert out == ""

    example_dtu_config.get_option("test", "option_that_does_not_exists")
    assert len(recwarn) == 1

    example_dtu_config.get_option("test", "integer") == "0"


def test_file_integrity(example_dtu_config, path):
    """
    Check that creating an object does not corrupt the existing configuration file

    We might want to check the same for other actions.
    """
    # create file
    example_dtu_config.save()
    text1 = example_dtu_config._read_config()

    # create new config object at the same path
    config2 = DTU_config.DtuConfig(path)
    # we haven't finalised the config yet

    # check that the new object read the file rather than erasing it.
    assert text1 == config2._read_config()
