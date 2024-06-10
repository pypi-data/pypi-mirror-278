"""Configuration class."""

import argparse
import os
import warnings
from configparser import ConfigParser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import phonenumbers
from appdirs import user_config_dir
from pydantic import AnyHttpUrl, EmailStr, validate_call

# =============================================================================
# Help functions to check the input types and validity
# =============================================================================


@validate_call
def _is_pydantic_url(value: AnyHttpUrl):
    """Use function.validate(arg) to check user input."""
    pass


@validate_call
def _is_pydantic_bool(value: bool):
    """Use function.validate(arg) to check user input."""
    pass


@validate_call
def _is_pydantic_str(value: str):
    """Use function.validate(arg) to check user input."""
    pass


@validate_call
def _is_pydantic_int(value: int):
    """Use function.validate(arg) to check user input."""
    pass


@validate_call()
def _is_pydantic_email(value: EmailStr):
    """Use function.validate(arg) to check user input."""
    pass


@validate_call
def is_valid_phone_number(value: str):
    """Validate a phone number using phonenumbers.parse."""
    parsed_number = phonenumbers.parse(value)
    return phonenumbers.is_valid_number(parsed_number)


def _get_valid_input(
    validator, prompt_text, value=None, default=None, limit=5, required=True
):
    """
    Ask for input until the value pass the validator or limit of tries exeeded.

    Parameters
    ----------
    validator : function
        Returns True is the input is adapted.
    prompt_text : str
        Text to prompt the user for another input.
    value : str, int, or bool, optional.
        Initial proposition for the value. The default is None.
    default: str, int or bool
        default proposition for the value, used if user enters nothing.
    limit : int, optional
        Number of times to ask for input before throwing an error. The default is 5.
    required : bool, optional
        Whether the value is required from the user.

    Returns
    -------
    value : str, int, or bool
        value that pass the validator.

    """

    i = 0
    while i < limit:
        try:
            # start by asking value unless we get user input the first time
            if (i > 0) or value is None:
                value = input(prompt_text).strip() or default
            validator(value)
            return value
        except ValueError as e:
            i += 1
            # if value is not required, accept None as an answer after first input
            if (value is None) and (not required):
                return None
            print(e)
            if not required:
                print("Press enter to skip.")


def _check_url_working(url):
    """Validate that the requested url is responding.

    Parameters
    ----------
    url : string
        Path to the license server, including port
    """
    check_text = (
        "Please check that you have entered the url correctly. "
        "If this issue persists contact your local license server administrator."
    )

    try:
        res = urlopen(url)
    except URLError:
        raise ConnectionError(f"Could not connect to {url}. {check_text}")

    if res.status != 200:
        raise ConnectionError(f"Could not connect to {url}. {check_text}")


# =============================================================================
# Main class
# =============================================================================


class DtuConfig:
    """
    Class for creation and manipulation of the application configuration file.

    Parameters
    ----------
    path : str or Path, optional
        Path to the application configuration file.
        Using app name and author is recommended for portability but path will
        have precedence if given.
    app_name: str, optional
        Name of the application
    app_author: str, optional
        Author of the application. Used for Windows path.
    """

    def __init__(self, path=None, app_name=None, app_author=None):
        """See class documentation."""
        # check that we have enough information for the path
        if not (path or app_name and app_author):
            raise ValueError(
                "Cannot create configuration: parameters should include the path of "
                "the configuration or the application name and author."
            )
        # name/author will be used only if path is not given.
        if not path:
            path = f"{user_config_dir(app_name, app_author)}/{app_name}.ini"
        self.path = Path(path)
        self._options = {}
        self._config = ConfigParser()
        if self.path.exists():
            self._config.read(self.path)

    # =========================================================================
    # add options to the object
    # =========================================================================

    def _add_option(self, section, option, **kwargs):
        kwargs["is_set"] = self._config.has_option(section, option)

        if section not in self._options.keys():
            self._options[section] = {option: kwargs}
        else:
            self._options[section][option] = kwargs

    def _add_general(
        self,
        section,
        option,
        pydantic_type,
        input_text,
        default,
        required,
        validator,
    ):
        if input_text is None:
            input_text = f"Please enter {option}"
            if not required:
                input_text = f"{input_text} (optional)"
        if default is not None:
            input_text = f"{input_text} [default: {default}]"
        input_text = f"{input_text} \n"

        self._add_option(
            section,
            option,
            pydantic_type=pydantic_type,
            input_text=input_text,
            default=default,
            required=required,
            validator=validator,
        )

    def add_url(
        self,
        section,
        option,
        pydantic_type=AnyHttpUrl,
        input_text="Please enter a valid URL.",
        default=None,
        required=True,
    ):
        """
        Add a url to the configuration.

        By default the method checks that the url is valid. This will fail if
        the user is offline.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str
            prompt
        """

        def validator(value):
            _is_pydantic_url(value)
            _check_url_working(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    def add_bool(
        self,
        section,
        option,
        pydantic_type=bool,
        input_text=None,
        default=None,
        required=True,
    ):
        """
        Add a boolean parameter to the configuration.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str
            prompt. If None, a default value will be created: "Please enter
            {option}"
        """

        def validator(value):
            _is_pydantic_bool(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    def add_str(
        self,
        section,
        option,
        pydantic_type=str,
        input_text=None,
        default=None,
        required=True,
    ):
        """
        Add a string parameter to the configuration.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str, optional
            prompt. If None, a default value will be created: "Please enter
            your {option}"
        """
        if input_text is None:
            input_text = f"Please enter your {option}"
            if not required:
                input_text = f"{input_text} (optional)"

        def validator(value):
            _is_pydantic_str(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    def add_int(
        self,
        section,
        option,
        pydantic_type=int,
        input_text=None,
        default=None,
        required=True,
    ):
        """
        Add an integer parameter to the configuration.

        To add constraints on the value please define a custom validator.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str
            prompt. If None, a default value will be created: "Please enter
            {option}"
        """

        def validator(value):
            _is_pydantic_int(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    def add_email(
        self,
        section,
        option,
        pydantic_type=EmailStr,
        input_text="Please enter your email adress.",
        default=None,
        required=True,
    ):
        """
        Add an email to the configuration.

        The method checks that the email has a valid format but not if it
        exists. To do so, send a confirmation email to the user.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str
            prompt
        """

        def validator(value):
            _is_pydantic_email(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    def add_phone_number(
        self,
        section,
        option,
        pydantic_type="phone_number",
        input_text="Please enter your phone number.",
        default=None,
        required=True,
    ):
        """
        Add a phone number to the configuration.

        By default the method checks if the number is valid. country code is
        required. To change requirements please define a default validator.

        Parameters
        ----------
        section: str
            String representing the configuration file section
        option : str
            Option of the configuration section that is being updated
        value : int, float or str
            Parameter value
        input_text : str
            prompt
        """

        def validator(value):
            is_valid_phone_number(value)

        self._add_general(
            section, option, pydantic_type, input_text, default, required, validator
        )

    # =========================================================================
    # create and edit the configuration
    # =========================================================================

    def create_config(self):
        """
        Create configuration.

        The user will be asked the values od the parameters that have not been
        saved.
        """
        conf = self._config

        # Loop over all options in the dataset
        for sec, opt_dict in self._options.items():
            if not conf.has_section(sec):
                conf.add_section(sec)
            for opt, meta in opt_dict.items():
                if not meta["is_set"]:
                    # Get user input and run checks:
                    # Pydantic & additional checks like URL is reachable
                    try:
                        val = _get_valid_input(
                            meta["validator"],
                            meta["input_text"],
                            default=meta["default"],
                            required=meta["required"],
                        )
                        if val:
                            conf[sec][opt] = str(val)
                            meta["is_set"] = True
                    except ValueError as e:
                        print(e)
        self.save()
        return conf

    def save(self):
        """Save the configuration file in the application directory."""
        if not os.path.isdir(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as config_file:
            self._config.write(config_file)

    def _read_config(self):
        """Load configuration file to DtuConfig class."""
        self._config.read(self.path)

    def finalise(self):
        """
        Remove _config sections/options that are not defined in _options.

        The configuration file is updated with the current options and saved.
        """
        for section in self._config.sections():
            # delete unused sections
            if section not in self._options:
                self._config.remove_section(section)
            # delete unused options
            else:
                for option in self._config[section]:
                    if option not in self._options[section]:
                        self._config.remove_option(section, option)
        self.save()

    # =========================================================================
    # parser and command line tool to edit the configuration
    # =========================================================================

    def _check_required_options(self):
        """Throw warnings if required options are not set."""
        for sec, opt_dict in self._options.items():
            for key in self._options[sec].keys():
                meta = opt_dict[key]
                if meta["required"] and not meta["is_set"]:
                    warnings.warn(
                        f"Option {key} of section {sec} is required and not set."
                    )

    def _create_parser(self):
        """Build ArgumentParser using settings of config object."""
        parser = argparse.ArgumentParser(
            description="Update configuration file", conflict_handler="resolve"
        )

        for section in self._options.keys():
            for key in self._options[section].keys():
                parser.add_argument(
                    f"--set-{section}-{key}",
                    help=f"Pass a value to section {section}, key {key}",
                )

        return parser.parse_args

    def cmd_tool(self, args=None):
        """Use argparse to values from the user."""
        pars = self._create_parser()
        if args:
            args = pars(args)
        else:
            args = pars()

        # process arguments from the user
        conf = self._config

        for sec, opt_dict in self._options.items():
            for key in self._options[sec].keys():
                if args.__dict__[f"set_{sec}_{key}"] is not None:
                    if not conf.has_section(sec):
                        conf.add_section(sec)
                    meta = opt_dict[key]
                    # Pydantic & additional checks like URL is reachable
                    try:
                        val = _get_valid_input(
                            meta["validator"],
                            meta["input_text"],
                            value=args.__dict__[f"set_{sec}_{key}"],
                            required=meta["required"],
                            default=meta["default"],
                        )
                        if val:
                            conf[sec][key] = str(val)
                            meta["is_set"] = True
                    except ValueError as e:
                        print(e)

        # Throw warning if required options are not set
        self._check_required_options()

        # Save config to disk
        self.save()

    # =========================================================================
    # get options from the object, view the content of the configuration
    # =========================================================================

    def get_option(self, section, option):
        """Return the value of the option if it is set or None."""
        if section not in self._options:
            warnings.warn(f"The section {section} does not exists.")
        if option not in self._options[section]:
            warnings.warn(f"The option {option} does not exists in section {section}")

        try:
            return self._config[section][option]
        except KeyError:
            return None

    def __str__(self):
        """Return configuration contents."""
        separator1 = "\n==="
        separator2 = "===\n"
        out = ""
        out += f"{separator1} SECTIONS {separator2}"
        for k, v in self._config.items():
            out += f"{k} {v}\n"
        out += "\n"
        for section, _ in self._config.items():
            out += f"{separator1} {section} {separator2}"
            # print keys, values
            for k, v in self._config.items(section):
                out += f"{k} {v}\n"
        return out

    def __repr__(self):
        """Return configuration contents."""
        return self.__str__()

    def show_options(self):
        """Print options dictionary."""
        separator1 = "\n==="
        separator2 = "===\n"
        out = ""
        out += f"{separator1} SECTIONS {separator2}"
        for sect in self._options:
            out += f"{sect}\n"
        for section in self._options:
            out += f"{separator1} {section} {separator2}"
            # print keys, values
            for opt in self._options[section]:
                out += f"{opt} {self._options[sect][opt]['pydantic_type']}\n"
        print(out)


if __name__ == "__main__":
    app_name = "pywasp"  # to modify
    app_author = "author"  # to modify

    # creation of object. If a file exists, it's loaded
    conf = DtuConfig(app_name=app_name, app_author=app_author)

    # add options. If  they have been set previously the user won't be asked
    # the values again.
    conf.add_int("test", "integer", default="0")
    conf.add_str("test", "string", default="Test string")
    conf.create_config()
    conf.finalise()

    # command interface
    conf.cmd_tool(args=["--set-test-string", "hi"])

    # print(conf)
    conf.show_options()
