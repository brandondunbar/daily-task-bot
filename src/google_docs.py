from jinja2 import Template


def render_template_to_string(template_str, row):
    """
    Render a template string with values from a task row.

    Args:
        template_str (str): A Jinja2 template string.
        row (dict): A dictionary containing values to inject into the template.

    Returns:
        str: The rendered string.
    """
    template = Template(template_str)
    return template.render(**row)


def create_google_doc(config, row):
    """
    Render content from a template and create a Google Doc in the specified folder.

    Args:
        config (dict): Contains `output_folder_id` and `template_blurb` keys.
        row (dict): A row of task data from the sheet.

    Returns:
        str: The ID of the created Google Doc.
    """
    content = render_template_to_string(config["template_blurb"], row)
    title_template = config.get("title_template", "{{ Date }}")
    title = render_template_to_string(title_template, row)
    folder_id = config["output_folder_id"]
    return _create_doc_in_drive(folder_id, title, content)


def _create_doc_in_drive(folder_id, title, content):
    """
    Placeholder function to represent the Google Docs API document creation.

    Args:
        folder_id (str): Google Drive folder ID.
        title (str): Title for the new Google Doc.
        content (str): Body content for the document.

    Returns:
        str: Document ID (placeholder).
    """
    raise NotImplementedError("Google Docs creation not implemented yet.")
