from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="verizon",
    asn_patterns=["verizon"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(query_term_list=["verizon"]),
)
