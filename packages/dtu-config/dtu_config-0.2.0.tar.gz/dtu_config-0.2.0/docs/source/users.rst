.. _users_guide:

Installation
============
To use the project, clone the `repository <https://gitlab-internal.windenergy.dtu.dk/ram/software/project-config>`_
and run the following commands:

.. code-block:: console

	$ cd path/to/project-config/
	$ pip install .

(pip and conda packages available soon)


Usage
=====

.. code-block:: python

    # Creation of object. If a file exists, it is loaded

    from dtu_config import DtuConfig
    app_name = "example_app"
    app_author = "author_name"
    conf = DtuConfig(app_name=app_name, app_author=app_author)

    # Add options.

    conf.add_str(
        "User metadata", "institution",
        input_text="Please enter your institution"
    )
    conf.add_email(
        "User metadata", "email",
        input_text="Please enter your email (optional)",
        required=False
    )

    # Create the configuration. If the options have been set previously, the user
    # will not be asked the values again, but they will be able to change them
    # from the command line tool.

    conf.create_config()

    # Calling finalise deletes unsused argmuments from previous versions of the
    # config file.

    conf.finalise()

    # Call the command line tool.

    conf.cmd_tool()
