import pytest
from src.template import render_template
from pathlib import Path


def test_render_template(tmp_path):
    # Create a temporary template file
    template_content = "Hello, {{ name }}!"
    template_path = tmp_path / "test_template.md"
    template_path.write_text(template_content)

    # Define context
    context = {"name": "Brandon"}

    # Render
    result = render_template(template_path, context)

    assert result == "Hello, Brandon!"
