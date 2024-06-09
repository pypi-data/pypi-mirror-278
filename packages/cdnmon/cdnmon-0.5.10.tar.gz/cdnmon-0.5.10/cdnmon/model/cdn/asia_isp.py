from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="asia-isp",
    asn_patterns=["asia-isp"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cy-isp.com", pattern=r"${domain}.cy-isp.com", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["asia-isp"]),
)
