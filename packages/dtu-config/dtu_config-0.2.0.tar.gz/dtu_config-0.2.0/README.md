# DTU Configuration

This package provides a configuration class to get, process, edit and store user input.


It is a thin wrapper around ConfigParser that provides utilities for adding validated configuration options and prompting the user for them, or allowing them to be filled by a CLI.

### Usage


```python

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
conf.create_config()
```
