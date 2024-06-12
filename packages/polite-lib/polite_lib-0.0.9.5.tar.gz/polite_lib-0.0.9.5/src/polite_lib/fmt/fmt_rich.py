"""
    Format Rich
    Polite Lib - Utils
    This module helps working with the Rich Cli display module

"""
from datetime import date
import logging

import arrow
from rich.table import Table


def fmt_value(thing) -> str:
    """Rich tables do not like values that are not strings."""
    if isinstance(list, thing):
        return ", ".join(thing)
    elif thing == 0:
        return str(0)
    if not thing:
        return ""
    if not isinstance(thing, str):
        return str(thing)
    return thing


def key_value_table(data: dict, title: str = None):
    """Create a Rich table with 2 columns. The first column as the key, the second column as the
    value.
    """
    if not data:
        logging.warning("Rich Fmt helper given no data")
        return False
    table = Table(title=fmt_value(title))
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for key, value in data.items():
        table.add_row(
            fmt_value(key),
            fmt_value(value))
    return table


# def key_value_financial_table(data: dict, title: str = None):
#     """Create a Rich table with 2 columns. The first column as the key, the second column as the
#     value.
#     """
#     if not data:
#         logging.warning("Rich Fmt helper given no data")
#         return False
#     table = Table(title=fmt_value(title))
#     table.add_column("Key", justify="left", no_wrap=True)
#     table.add_column("Value", justify="right", )
#     for key, value in data.items():
#         if isinstance(value, float) or isinstance(value, Decimal):
#             value = value
#         table.add_row(
#             fmt_value(key),
#             fmt_value(value))
#     return table


def rows_table(rows: list, title: str = None):
    """Create a Rich table from a list of data."""
    table = Table(title=fmt_value(title))
    columns = len(rows[0])
    for x in range(columns):
        if x != 0:
            table.add_column(justify="right")
        else:
            table.add_column("")
    data = []
    for row in rows:
        new_row = []
        for cell in row:
            new_row.append(fmt_value(cell))
        data.append(new_row)
    for row in data:
        table.add_row(*row)
    return table


def fmt_date(the_date, days_ago=False) -> str:
    """Attempt to format a date type of some flavor into something we want to show to the console.
    """
    if type(the_date) not in [arrow.Arrow, date]:
        logging.error("Bad type for fmt_date: %s" % type(the_date))
        return ""
    now = arrow.utcnow()
    try:
        the_date = arrow.get(the_date)
    except arrow.parser.ParserError as e:
        logging.error("Format date error. input: %s, Exception %s" % (the_date, e))
        return ""
    the_days_ago = (now - the_date).days
    if the_date.year == now.year and days_ago < 365:
        the_format = "MMM D"
    else:
        the_format = "MMM D, YYYY"
    the_str = "%s" % the_date.format(the_format)
    if days_ago:
        the_str += " (%s days ago)" % the_days_ago
    return the_str


def fin_num_color(the_value: str) -> str:
    """Finacial Number Color
    Add Rich templated font colors to a financial numeric string.
    If the number has a "-" symbol, it's colored RED, otheriwse its GREEN.
    """
    if not the_value:
        return ""
    if "-" in the_value:
        return "[red]%s[/red]" % the_value
    else:
        return "[green]%s[/green]" % the_value


# End File: polite-lib/src/polite-lib/utils/fmt_rich.py
