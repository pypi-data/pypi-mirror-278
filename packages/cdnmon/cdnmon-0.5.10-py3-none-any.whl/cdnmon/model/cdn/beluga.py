from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="beluga",
    asn_patterns=["beluga"],
    cname_suffixes=[
        CNAMEPattern(suffix=".belugacdn.com", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["beluga"]),
)
