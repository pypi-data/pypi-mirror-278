from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdnsun",
    asn_patterns=["cdnsun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".r.cdn.net"),
        CNAMEPattern(suffix=".cdnsun.net", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["cdnsun"]),
)
