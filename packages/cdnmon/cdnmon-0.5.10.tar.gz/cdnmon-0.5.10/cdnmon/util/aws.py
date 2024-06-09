import ipaddress

import requests


def get_ip_range_of_aws(pattern):
    data = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json").json()

    ipv4_networks = []
    ipv4_prefixes = data["prefixes"]
    for ipv4_prefix in ipv4_prefixes:
        if ipv4_prefix["service"] == pattern:
            ipv4_networks.append(str(ipaddress.IPv4Network(ipv4_prefix["ip_prefix"], strict=False)))

    ipv6_networks = []
    ipv6_prefixes = data["ipv6_prefixes"]
    for ipv6_prefix in ipv6_prefixes:
        if ipv6_prefix["service"] == pattern:
            ipv6_networks.append(str(ipaddress.IPv6Network(ipv6_prefix["ipv6_prefix"], strict=False)))

    return ipv4_networks, ipv6_networks
