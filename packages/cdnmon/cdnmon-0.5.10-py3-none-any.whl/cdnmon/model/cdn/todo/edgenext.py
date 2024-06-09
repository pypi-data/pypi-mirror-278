from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="edgenext",
    asn_patterns=["edgenext"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["edgenext"]),
)
