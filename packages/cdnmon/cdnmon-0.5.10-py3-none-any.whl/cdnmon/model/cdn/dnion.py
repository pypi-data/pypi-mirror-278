from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="dnion",
    asn_patterns=["dnion"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ayhtbj.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".ayhtbj.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".dnion.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".dnion.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".globalcdn.com.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".goidns.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".grdunion.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".mcadn.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".prdxg.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".ttxshy.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".tvayht.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".tvayht.net", source="https://beian.miit.gov.cn/"),
    ],
    cidr=BGPViewCIDR(["dnion"]),
)
