"""
    Polite Lib
    Utils
    Network Tools

"""
import logging
import random
import subprocess

import requests


def ping(host: str = "1.1.1.1", count: int = 1) -> dict:
    """Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', "-c", str(count), host]
    print(command)
    result = subprocess.check_output(command).decode()
    result = result.split("\n")
    stat_line = count + 3
    packet_loss = result[stat_line][result[stat_line].find("received,") + 10:result[stat_line].rfind(" packet loss")]
    ret = {
        "packet_loss": packet_loss,
        "avg": 0,

    }
    return ret


def get_ip() -> str:
    """Get the WAN IP address of the device."""
    wan_ip_apis = [
        "https://ip.seeip.org/jsonip?",
        "https://api.ipify.org/?format=json",
        "https://api.my-ip.io/ip.json",
        "http://icanhazip.com"
    ]
    api_number = random.randint(0, len(wan_ip_apis))
    current_wan_ip = ""
    while current_wan_ip == "":
        api_number = random.randint(0, len(wan_ip_apis) - 1)
        current_wan_ip = _attempt_to_get_ip(wan_ip_apis[api_number])
        del wan_ip_apis[api_number]
    return current_wan_ip


def _attempt_to_get_ip(api_url: str):
    logging.debug('Getting IP from: %s' % api_url)
    if api_url == "http://icanhazip.com":
        return _get_wan_ip_from_icanhazip(api_url)
    else:
        return _get_wan_ip_from_generic_api(api_url)


def _get_wan_ip_from_generic_api(url: str):
    response = _make_request(url)
    if not response:
        return ''
    response_j = response.json()
    return response_j['ip']


def _get_wan_ip_from_icanhazip(url: str):
    response = requests.get(url)
    current_ip = response.text.replace("\n", "")
    return current_ip


def _make_request(url: str):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error('Connection failed to: %s' % url)
        return ''
    if str(response.status_code)[0] != '2':
        logging.error('Bad Response of "%s" from %s' % (response.status_code, url))
        return ''
    return response

# End File: polite-lib/src/polite-lib/utils/network_tools.py
