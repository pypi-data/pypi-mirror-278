from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="yottaa",
    asn_patterns=["yottaa"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".yottaa.net",
            pattern=r"${random}.yottaa.net",
            example="fc15a390abd40137aa767e3461d3e37f.yottaa.net",
            source="https://docs.yottaa.com/Content/CNAME%20Usage.htm",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["yottaa"]),
)
