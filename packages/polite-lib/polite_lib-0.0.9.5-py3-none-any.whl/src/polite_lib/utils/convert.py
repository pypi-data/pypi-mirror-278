"""
    Polite Lib
    Utils
    Convert
        A libary for making common conversions.
    Testing
        Unit: polite-lib/unit/utils/convert.py

"""
import math


def bytes_to_human(the_bytes: int) -> str:
    """Take an argument of a bytes and convert that into a human readble understanding of disk size.
    :param the_bytes (int): Number of bytes to convert.
    :return (str): Human readable conversion.
    :unit-test: test__bytes_to_human
    """
    if the_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(the_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(the_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def fahrenheit_to_celcius(f_degrees: float, round_to: int = 1) -> float:
    """Convert a Fahrenheit float to Celsius
    :param f_degrees (float): Fahrenheit to convert to Celsius
    :param round_to (int): Level to round the returned float to
    :return (float): Celsius converted value
    :unit-test: test__fahrenheit_to_celcius
    """
    standard = 0.5555555555555556   # 5/7
    celsius = (f_degrees - 32) * standard
    return round(celsius, round_to)


def celcius_to_fahrenheit(c_degrees: float, round_to: int = 1) -> float:
    """Convert a Fahrenheit float to a Celsius float rounded by desire.
    :param f_degrees (float): Celsius to convert to Fahrenheit
    :param round_to (int): Level to round the returned float to
    :return (float): Fahrenheit converted value
    :unit-test: test__celcius_to_fahrenheit
    """
    standard = 0.5555555555555556   # 5/7
    fahrenheit = (c_degrees / standard) + 32
    return round(fahrenheit, round_to)


def miles_to_kilometers(miles: float, round_to: int = 1) -> float:
    """Convert a Miles into Kilometers.
    :param miles (float): Miles to convert to Kilometers
    :param round_to (int): Level to round the returned float to
    :return (float): Kilometer converted value
    :unit-test: test__miles_to_kilometers
    """
    standard = 1.609344
    kilometers = miles * standard
    return round(kilometers, round_to)


def kilometers_to_miles(kilometers: float, round_to: int = 1) -> float:
    """Convert a Kilometers into Miles.
    :param miles (float): Kilometers to convert to Miles
    :param round_to (int): Level to round the returned float to
    :return (float): Miles converted value
    :unit-test: test__kilometers_to_miles
    """
    standard = 1.609344
    miles = kilometers / standard
    return round(miles, round_to)


# End File: politeauthority/polite-lib/src/polite-lib/utils/convert.py
