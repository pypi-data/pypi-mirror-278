from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.util.cidr import deduplicate_networks


class MaxCDNCIDR(CIDR):
    ipv4_url: str = "https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt"
    ipv6_url: str = ipv4_url

    def extract(self):
        """
        [1] https://support.maxcdn.com/one/tutorial/ip-blocks/
        [2] https://support.maxcdn.com/one/assets/ips.txt (302 Redirected to [3])
        [3] https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt
        """
        text = self.http_get(self.ipv4_url).text
        return {
            "ipv4": text,
            "ipv6": text,
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }


CDN = CommonCDN(
    name="maxcdn",
    asn_patterns=["maxcdn"],
    cname_suffixes=[
        CNAMEPattern(suffix=".netdna-cdn.com"),
        CNAMEPattern(suffix=".netdna-ssl.com"),
        CNAMEPattern(suffix=".netdna.com"),
    ],
    cidr=MaxCDNCIDR(),
)
