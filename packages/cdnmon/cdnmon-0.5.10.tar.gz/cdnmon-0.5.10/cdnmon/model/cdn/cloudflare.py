from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification
from cdnmon.util.cidr import deduplicate_networks


class CloudflareCIDR(CIDR):
    ipv4_url: str = "https://www.cloudflare.com/ips-v4"
    ipv6_url: str = "https://www.cloudflare.com/ips-v6"

    def extract(self):
        return {
            "ipv4": self.http_get(self.ipv4_url).text,
            "ipv6": self.http_get(self.ipv6_url).text,
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }


CDN = CommonCDN(
    name="cloudflare",
    asn_patterns=["cloudflare"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdn.cloudflare.net", pattern=r"${domain}.cdn.cloudflare.net", is_leaf=True),
    ],
    cidr=CloudflareCIDR(),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="cloudflare-verify",
            pattern=r"[0-9]{8}-[0-9]{8}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
