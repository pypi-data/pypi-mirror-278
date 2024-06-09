from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="hubspot",
    asn_patterns=["hubspot"],
    cname_suffixes=[
        CNAMEPattern(suffix=".hubspot.net", source="https://www.hubspot.com/products/cms/cdn", is_leaf=False),
        CNAMEPattern(suffix=".sites.hscoscdn00.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdn10.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdn20.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdn30.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdn40.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdnqa00.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdnqa10.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdnqa20.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdnqa30.net", is_leaf=True),
        CNAMEPattern(suffix=".sites.hscoscdnqa40.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["hubspot"]),
)
