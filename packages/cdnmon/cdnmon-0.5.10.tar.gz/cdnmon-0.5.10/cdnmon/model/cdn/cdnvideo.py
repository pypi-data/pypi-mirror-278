from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdnvideo",
    asn_patterns=["cdnvideo"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".a.trbcdn.net",
            source="https://doc.cdnvideo.ru/en/Services_setup/http/",
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["cdnvideo"]),
)
