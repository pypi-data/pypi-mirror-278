import IPy


def deduplicate_networks(networks, filter_version=4):
    deduplicated_networks = IPy.IPSet(
        [
            IPy.IP(str(network), make_net=1)
            for network in networks
            if IPy.IP(str(network), make_net=1).version() == filter_version
        ]
    )
    deduplicated_networks.optimize()
    return [str(network) for network in deduplicated_networks]
