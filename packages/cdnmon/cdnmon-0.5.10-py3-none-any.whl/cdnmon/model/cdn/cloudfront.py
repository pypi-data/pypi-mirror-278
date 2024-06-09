from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.util.aws import get_ip_range_of_aws
from cdnmon.util.cidr import deduplicate_networks


class CloudFrontCIDR(CIDR):
    ipv4_url: str = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    ipv6_url: str = ipv4_url

    def extract(self):
        """
        [1] https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
        """
        ipv4_networks, ipv6_networks = get_ip_range_of_aws("CLOUDFRONT")
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
    name="cloudfront",
    asn_patterns=["cloudfront", "amazon"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cloudfront.net", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".cloudfront.cn"),
    ],
    cidr=CloudFrontCIDR(),
)
