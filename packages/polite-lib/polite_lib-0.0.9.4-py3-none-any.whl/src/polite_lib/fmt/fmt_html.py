"""
    Polite Lib
    Html
    Tools for writing html

"""

from ..utils import xlate


def anchor(url: str, title: str = None) -> str:
    """Create an anchor link in html with a given anchor and title string to use.
    :unit-test: TestFmtHtml::test__anchor
    """
    if not title:
        title = url
    return '<a href="%s">%s</a>' % (url, title)


def code(the_code: str) -> str:
    """Wrap the text in a <code> tags.
    :unit-test: TestFmtHtml::test__code
    """
    if not the_code:
        return ""
    return f"<code>{the_code}</code>"


def strip_markup(original: str) -> str:
    """Strip certain HTML markup tags. Curretly removes <br> tags manually, and everyting that
    xlate.filter_html_tags replaces.
    :unit-test: TestFmtHtml::test__strip_markup
    """
    if not original:
        return ""
    stripped = original
    if "<br>" in original:
        stripped = original.replace("<br>", " ")
    if "<br/>" in original:
        stripped = original.replace("<br>", " ")
    stripped = xlate.filter_html_tags(stripped)
    return stripped


def table_from_dict(the_dict: dict, t_format=["bold_key"]) -> str:
    """Create a vertical html table from a dictonary."""
    if not the_dict:
        return ""
    table = "<table>"
    for key, value in the_dict.items():
        key_print = key
        if "bold_key" in t_format:
            key_print = "<b>%s</b>" % key_print
        table += "<tr><td>%s</td><td>%s</td></tr>" % (key_print, str(value))
    table += "</table>"
    return table


def unordered_list(the_list: list) -> str:
    """Create a vertical html table from a dictonary."""
    if not the_list:
        return "<ul><ul>"
    html = "<ul>"
    for item in the_list:
        html = "  <li>%s</li>" % item
    html += "</ul>"
    return html

# End File: politeauthority/polite-lib/src/polite-lib/utils/fmt_html.py
