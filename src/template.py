"""Template rendering utilities for generating document content.

This module provides a helper to load a Jinja2 template from disk and render
it with a given context dictionary.
"""

from pathlib import Path
from typing import Any, Dict

from jinja2 import Template


def render_template(template_path: Path, context: Dict[str, Any]) -> str:
    """Render a Jinja2 template file with the provided context.

    Reads the template file from `template_path`, compiles it, and substitutes
    variables using the keys/values in `context`.

    Args:
        template_path: Filesystem path to the Jinja2 template file.
        context: Dictionary of variables to inject into the template.

    Returns:
        The rendered template as a string.

    Raises:
        FileNotFoundError: If the template file does not exist.
        jinja2.TemplateSyntaxError: If the template contains invalid syntax.
    """
    with open(template_path, 'r') as file:
        template_str = file.read()

    template = Template(template_str)
    return template.render(**context)
