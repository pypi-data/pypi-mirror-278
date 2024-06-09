#
from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="blazingcdn",
    asn_patterns=["blazing"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".blazingcdn.net",
            pattern=r"cdn${random-number}.blazingcdn.net",
            example="cdn55449950.blazingcdn.net",
            source="https://knowledgebase.blazingcdn.com/get-started-complete-guide/",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["blazingcdn"]),
)
