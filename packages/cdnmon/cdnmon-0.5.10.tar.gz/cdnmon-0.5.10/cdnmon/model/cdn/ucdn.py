from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="ucdn",
    asn_patterns=["ucdn"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".b.cdn12.com",
            pattern=r"${random}.b.cdn12.com",
            example="11011-10.b.cdn12.com",
            source="https://help.ucdn.com/how-can-i-add-a-cname-record-to-my-cdn-zone/",
            is_leaf=True,
            is_root=True,
        ),
        CNAMEPattern(
            suffix=".b.cdn13.com",
            pattern=r"${random}.b.cdn13.com",
            example="11011-10.b.cdn13.com",
            source="https://help.ucdn.com/how-can-i-add-a-cname-record-to-my-cdn-zone/",
            is_leaf=True,
            is_root=True,
        ),
    ],
    cidr=BGPViewCIDR(["ucdn"]),
)
