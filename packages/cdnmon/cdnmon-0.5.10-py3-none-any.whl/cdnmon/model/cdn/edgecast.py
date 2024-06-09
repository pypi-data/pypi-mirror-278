from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="edgecast",
    asn_patterns=["edgecast"],
    cname_suffixes=[
        CNAMEPattern(suffix=".edgecastcdn.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["edgecast"]),
)
