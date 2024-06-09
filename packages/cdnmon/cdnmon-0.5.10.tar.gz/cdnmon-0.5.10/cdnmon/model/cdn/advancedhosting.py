from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="advancedhosting",
    asn_patterns=["advancedhosting"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ahacdn.me", source="https://advancedhosting.com/en/wiki/anycast-cdn/api/", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["advancedhosting"]),
)
