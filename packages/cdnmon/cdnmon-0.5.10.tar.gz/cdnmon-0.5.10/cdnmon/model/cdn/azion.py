from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="azion",
    asn_patterns=["azion"],
    cname_suffixes=[
        CNAMEPattern(suffix=".map.azionedge.net", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".azioncdn.net", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".azioncdn.com"),
        CNAMEPattern(suffix=".azion.net"),
    ],
    cidr=BGPViewCIDR(["azion"]),
)
