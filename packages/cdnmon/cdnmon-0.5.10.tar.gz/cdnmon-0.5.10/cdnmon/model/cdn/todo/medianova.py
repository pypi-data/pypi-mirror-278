from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="medianova",
    asn_patterns=["medianova"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(query_term_list=["medianova"]),
)
# *.mncdn.com
# *.mncdn.net
# *.mncdn.org
