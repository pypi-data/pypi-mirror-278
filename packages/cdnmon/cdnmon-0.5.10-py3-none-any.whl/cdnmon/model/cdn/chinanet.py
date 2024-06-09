from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="chinanet",
    asn_patterns=["chinanet"],
    cname_suffixes=[
        CNAMEPattern(suffix=".iname.damddos.com", pattern=r"${domain}.iname.damddos.com", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["chinanet"]),
)
