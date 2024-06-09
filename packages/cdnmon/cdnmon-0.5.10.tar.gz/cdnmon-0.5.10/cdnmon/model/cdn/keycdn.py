from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="keycdn",
    asn_patterns=["keycdn"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".kxcdn.com",
            source="https://www.keycdn.com/support/cdn-integration",
            is_leaf=True,
            is_root=True,
        ),
        CNAMEPattern(suffix=".kvcdn.com"),
    ],
    cidr=BGPViewCIDR(["keycdn"]),
)
