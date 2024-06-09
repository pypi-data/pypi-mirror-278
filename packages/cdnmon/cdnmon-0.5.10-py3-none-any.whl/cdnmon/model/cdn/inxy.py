from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="inxy",
    asn_patterns=["inxy"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdn.inxy.com", source="https://dev.inxy.hosting/help-center/help-cdnnow/"),
        CNAMEPattern(
            suffix=".hwcdn.net",
            source="https://dev.inxy.hosting/help-center/help-highwinds-cdn/",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["inxy"]),
)
