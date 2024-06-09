from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="lumen",
    asn_patterns=["lumen"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(query_term_list=["lumen"]),
)
