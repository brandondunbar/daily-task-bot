from jinja2 import Template
from pathlib import Path


def render_template(template_path: Path, context: dict) -> str:
    """
    Render a Jinja2 template file using the provided context dictionary.

    Args:
        template_path (Path): Path to the template file.
        context (dict): Dictionary of values to inject into the template.

    Returns:
        str: Rendered template string.
    """
    with open(template_path, 'r') as file:
        template_str = file.read()

    template = Template(template_str)
    return template.render(**context)
