from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="bunny",
    asn_patterns=["bunny"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".b-cdn.net",
            source="https://support.bunny.net/hc/en-us/articles/207790279-How-to-set-up-a-custom-CDN-hostname",
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["bunny"]),
)
