from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="imperva",
    asn_patterns=["imperva"],
    cname_suffixes=[
        CNAMEPattern(suffix=".impervadns.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["imperva"]),
)
