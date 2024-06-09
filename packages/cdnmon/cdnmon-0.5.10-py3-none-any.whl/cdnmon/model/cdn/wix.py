from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="wix",
    asn_patterns=["wix"],
    cname_suffixes=[
        CNAMEPattern(suffix=".wixdns.net", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["wix"]),
)
