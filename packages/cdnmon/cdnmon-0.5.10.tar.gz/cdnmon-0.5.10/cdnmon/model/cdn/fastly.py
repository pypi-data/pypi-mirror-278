from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification
from cdnmon.util.cidr import deduplicate_networks


class FastlyCIDR(CIDR):
    ipv4_url: str = "https://api.fastly.com/public-ip-list"
    ipv6_url: str = ipv4_url

    def extract(self):
        """
        [1] https://api.fastly.com/public-ip-list
        """
        import ipaddress

        data = self.http_get(self.ipv4_url).json()

        ipv4_networks = []
        for ipv4_prefix in data["addresses"]:
            ipv4_networks.append(str(ipaddress.IPv4Network(ipv4_prefix, strict=False)))

        ipv6_networks = []
        for ipv6_prefix in data["ipv6_addresses"]:
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
    name="fastly",
    asn_patterns=["fastly"],
    cname_suffixes=[
        CNAMEPattern(suffix=".global.ssl.fastly.net", pattern=r"${name}.global.ssl.fastly.net", is_leaf=True),
        CNAMEPattern(suffix=".freetls.fastly.net", pattern=r"${name}.freetls.fastly.net", is_leaf=True),
        CNAMEPattern(suffix=".global.prod.fastly.net", pattern=r"${domain}.global.prod.fastly.net", is_leaf=True),
        CNAMEPattern(suffix=".nonssl.global.fastly.net", pattern=r"nonssl.global.fastly.net", is_leaf=True),
        CNAMEPattern(suffix=".nonssl.us-eu.fastly.net", pattern=r"nonssl.us-eu.fastly.net", is_leaf=True),
        CNAMEPattern(suffix=".global.fastly.net", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".fastly.net"),
    ],
    cidr=FastlyCIDR(),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
