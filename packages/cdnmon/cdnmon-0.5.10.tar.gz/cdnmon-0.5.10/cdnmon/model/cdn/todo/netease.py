from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="netease",
    asn_patterns=["netease"],
    cname_suffixes=[
        CNAMEPattern(suffix=".163jiasu.com", pattern=r"${domain}.163jiasu.com"),
        CNAMEPattern(suffix=".ntes53.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["netease"]),
)
