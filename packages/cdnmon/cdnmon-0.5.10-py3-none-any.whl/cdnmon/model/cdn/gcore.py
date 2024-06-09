from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.util.cidr import deduplicate_networks


class GCoreCIDR(CIDR):
    ipv4_url: str = "https://api.gcore.com/cdn/public-ip-list"
    ipv6_url: str = ipv4_url

    def extract(self):
        """
        [1] https://apidocs.gcore.com/cdn#tag/IP-Addresses-List
        [2] https://api.gcorelabs.com/cdn/public-net-list
        """
        import ipaddress

        data = self.http_get(self.ipv4_url).json()

        ipv4_networks = []
        for ipv4_prefix in data["addresses"]:
            ipv4_networks.append(str(ipaddress.IPv4Network(ipv4_prefix, strict=False)))

        ipv6_networks = []
        for ipv6_prefix in data["addresses_v6"]:
            ipv6_networks.append(str(ipaddress.IPv6Network(ipv6_prefix, strict=False)))

        return {
            "ipv4": "\n".join(ipv4_networks),
            "ipv6": "\n".join(ipv6_networks),
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }


CDN = CommonCDN(
    name="gcore",
    asn_patterns=["gcore"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".gcdn.co",
            source="https://www.netify.ai/resources/domains/gcdn.co",
            example="cl-3249f890.gcdn.co",
            is_leaf=True,
        ),
    ],
    cidr=GCoreCIDR(),
)
