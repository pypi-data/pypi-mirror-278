from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="incapsula",
    asn_patterns=["incapsula"],
    cname_suffixes=[
        CNAMEPattern(suffix=".incapdns.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["incapsula"]),
)
