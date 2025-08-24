import pytest
from jinja2 import TemplateSyntaxError
from src.template import render_template


@pytest.mark.parametrize(
    "template_content, context, expected",
    [
        ("Hello, {{ name }}!", {"name": "Brandon"}, "Hello, Brandon!"),
        ("Hi {{ first }} {{ last }}.",
         {"first": "Vivi", "last": "Ornitier"}, "Hi Vivi Ornitier."),
        ("Hello, {{ name|default('Friend') }}!", {}, "Hello, Friend!"),
    ],
)
def test_render_template_parametrized(tmp_path, template_content, context, expected):
    """Renders various Jinja2 templates with different contexts and defaults."""
    template_path = tmp_path / "t.md"
    template_path.write_text(template_content, encoding="utf-8")
    assert render_template(template_path, context) == expected


def test_render_template_invalid_syntax(tmp_path):
    """Raises TemplateSyntaxError for invalid Jinja2 syntax."""
    bad_template = "Hello, {{ name "  # missing closing braces
    template_path = tmp_path / "bad.md"
    template_path.write_text(bad_template, encoding="utf-8")
    with pytest.raises(TemplateSyntaxError):
        render_template(template_path, {"name": "X"})


def test_render_template_missing_file(tmp_path):
    """Raises FileNotFoundError when the template file does not exist."""
    missing_path = tmp_path / "nope.md"
    with pytest.raises(FileNotFoundError):
        render_template(missing_path, {"a": 1})


def test_render_template_unicode_and_emoji(tmp_path):
    """Handles Unicode and emoji content correctly during rendering."""
    template_content = "こんにちは、{{ name }} 🌸"
    template_path = tmp_path / "unicode.md"
    template_path.write_text(template_content, encoding="utf-8")
    result = render_template(template_path, {"name": "太郎"})
    assert result == "こんにちは、太郎 🌸"
