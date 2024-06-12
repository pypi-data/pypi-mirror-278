"""
    Polite Lib
    Utils
    Format Numbers
    Testing
        Unit: polite-lib/unit/fmt/test_fmt_nums.py

"""
import logging


def add_commas(value) -> str:
    """
    Args:
        value: The integer or float value to format.
    :returns: A string with commas every 3 digits.
    :unit-test: test__add_commas
    """
    if value <= 999:
        return str(value)
    original_value_str = str(value)

    formatted_value = "{:,}".format(int(value))
    if "." in original_value_str:
        formatted_value += original_value_str[original_value_str.find("."):]
    return formatted_value


def fmt_currency(value: float, round_to: int = 2) -> str:
    """Format a float value to a USD currency representation.
    :unit-test: test__fmt_currency
    """
    if not value:
        logging.warning("fmt currency recieved null value")
        return ""
    value = round(value, round_to)
    value_str = str(value)
    value_commas = add_commas(value)
    # Add a leading 0 to values under a dollar
    if value < 1:
        if "." in value_str:
            dot_position = value_str.find(".")
            if dot_position == 0:
                value_str = "0" + value_str
    else:
        value_str = value_commas

    if "." in value_str:
        dot_position = value_str.find(".")
        if len(value_str) <= dot_position + round_to:
            value_str = value_str + "0"
    else:
        value_str = value_str + ".00"
    value_str = "$" + value_str
    return value_str


def fmt_percentage(value: float, round_to: int = 2) -> str:
    """Format a percentage into a human friendly string, rounded to the desired level.
    :unit-test: test__fmt_percentage
    """
    if not value:
        return None
    value = round(value, round_to)
    value_str = add_commas(value)

    # Add a leading 0 to values under a dollar
    if value < 1:
        if "." in value_str:
            dot_position = value_str.find(".")
            if dot_position == 0:
                value_str = "0" + value_str
    else:
        value_str = value_str

    if "." in value_str:
        dot_position = value_str.find(".")
        if len(value_str) <= dot_position + round_to:
            value_str = value_str + "0"
    else:
        value_str = value_str + ".00"

    if round_to == 0:
        value_str = value_str[:value_str.find(".")]

    return value_str + "%"


# End File: politeauthority/polite-lib/src/polite-lib/utils/fmt_numbers.py
