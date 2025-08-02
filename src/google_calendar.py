from jinja2 import Template


def render_template(template_str, row):
    """
    Render a Jinja2-style template using values from a task row.

    Args:
        template_str (str): Template string to render.
        row (dict): Data row with values for placeholders.

    Returns:
        str: Rendered string.
    """
    return Template(template_str).render(**row)


def create_calendar_event(config, row, doc_link):
    """
    Use config and row data to create a calendar event.

    Args:
        config (dict): Configuration including calendar settings.
        row (dict): Task data.
        doc_link (str): Link to the generated Google Doc.

    Returns:
        str: Calendar event ID (or placeholder).
    """
    cal_cfg = config.get("calendar", {})
    title_template = cal_cfg.get("title_template", "{{ problem_title }}")
    time = cal_cfg.get("time", "09:00")
    duration = cal_cfg.get("duration_minutes", 30)

    summary = render_template(title_template, row)
    description = f"Solve: {row.get('problem_title', '')} \
        {row.get('leetcode_link', '')}"

    return _create_event_on_calendar(summary, time, duration, description, doc_link)


def _create_event_on_calendar(summary, time, duration, description, doc_link):
    """
    Placeholder for Google Calendar API event creation.

    Args:
        summary (str): Event title.
        time (str): Start time (HH:MM).
        duration (int): Duration in minutes.
        description (str): Event description.
        doc_link (str): Link to associated Google Doc.

    Returns:
        str: ID of the created event.
    """
    raise NotImplementedError("Google Calendar integration not yet implemented.")
