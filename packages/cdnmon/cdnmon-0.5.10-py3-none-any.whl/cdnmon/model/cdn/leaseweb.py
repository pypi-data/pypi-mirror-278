from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="leaseweb",
    asn_patterns=["leaseweb"],
    cname_suffixes=[
        CNAMEPattern(suffix=".leasewebultracdn.com", pattern=r"di-[0-9a-z]{8}.leasewebultracdn.com"),
        CNAMEPattern(suffix=".lswcdn.net", pattern=r"di-[0-9a-z]{8}.pr.lswcdn.net"),
        CNAMEPattern(suffix=".llnwi.net", pattern=r"leaseweb.s.llnwi.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["leaseweb"]),
)
