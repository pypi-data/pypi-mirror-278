from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="qihoo",
    asn_patterns=["qihoo"],
    cname_suffixes=[
        CNAMEPattern(suffix=".360cdn.cn", pattern=r"${domain}.360cdn.cn"),
        CNAMEPattern(suffix=".360dlcdn.com", pattern=r"${domain}.360dlcdn.com"),
        CNAMEPattern(suffix=".360imgcdn.com", pattern=r"${domain}.360imgcdn.com"),
        CNAMEPattern(suffix=".360qhcdn.com", pattern=r"${domain}.360qhcdn.com", is_leaf=True),
        CNAMEPattern(suffix=".360tpcdn.com", pattern=r"${domain}.360tpcdn.com"),
        CNAMEPattern(suffix=".360wzb.cn", pattern=r"${domain}.360wzb.cn"),
        CNAMEPattern(suffix=".360wzb.com", pattern=r"${domain}.360wzb.com"),
        CNAMEPattern(suffix=".qh-cdn.com", pattern=r"${domain}.qh-cdn.com", is_root=False),
        CNAMEPattern(suffix=".qhcdn-lb.com", pattern=r"${domain}.qhcdn-lb.com"),
        CNAMEPattern(suffix=".qhcdn.com", pattern=r"${domain}.qhcdn.com", is_leaf=True),
        CNAMEPattern(suffix=".qhdlcdn.com", pattern=r"${domain}.qhdlcdn.com"),
        CNAMEPattern(suffix=".qihucdn.com", pattern=r"${domain}.qihucdn.com", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["qihoo"]),
)
