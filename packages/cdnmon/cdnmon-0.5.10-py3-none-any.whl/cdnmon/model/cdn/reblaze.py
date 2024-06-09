from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="reblaze",
    asn_patterns=["reblaze"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".rbzdns.com",
            source="https://gb.docs.reblaze.com/v/v2.14/product-walkthrough/settings/dns",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["reblaze"]),
)
