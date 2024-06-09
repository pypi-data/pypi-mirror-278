from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="sitelock",
    asn_patterns=["sitelock"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".sitelockcdn.net",
            source="https://www.sitelock.com/help-center/how-to-configure-your-trueshield-web-application-firewall-waf/",
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["sitelock"]),
)
