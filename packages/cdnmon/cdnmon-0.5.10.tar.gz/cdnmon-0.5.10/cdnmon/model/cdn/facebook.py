from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="facebook",
    asn_patterns=["facebook", "meta"],
    cname_suffixes=[
        CNAMEPattern(suffix="fbcdn.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["facebook", "meta"]),
)
