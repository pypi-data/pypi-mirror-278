from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="ngenix",
    asn_patterns=["ngenix"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".cdn.ngenix.net",
            pattern=r"s${random-number}.cdn.ngenix.net",
            source="https://docs.ngenix.net/integraciya-s-platformoi/podklyuchenie-veb-resursa/hto-wsa-cname",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["ngenix"]),
)
