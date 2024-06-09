from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="jingdong",
    asn_patterns=["jingdong"],
    cname_suffixes=[
        CNAMEPattern(suffix=".360buy.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cdinghuo.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cdinghuo.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cdn.jcloudcache.com", pattern=r"${domain}.lk-[0-9a-f]{6}.cdn.jcloudcache.com"),
        CNAMEPattern(suffix=".cdn.jcloudcdn.com", pattern=r"${domain}.cdn.jcloudcdn.com", is_leaf=True),
        CNAMEPattern(suffix=".cloud-scdn-ns.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-scdn-ns.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-scdn-ns.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-scdn-ns.tech", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-scdn.com", source="https://beian.miit.gov.cn/", is_leaf=True),
        CNAMEPattern(suffix=".cloud-starshield.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-starshield.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".cloud-starshield.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".dy.galileo.jcloud-cdn.com", pattern=r"${domain}.dy.galileo.jcloud-cdn.com"),
        CNAMEPattern(suffix=".gslb.qianxun.com", pattern=r"${domain}.gslb.qianxun.com", is_leaf=True),
        CNAMEPattern(suffix=".haiketong.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jcloud-cdn.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jcloudcache.com", pattern=r"${domain}.lk-[0-9a-f]{6}.jcloudcache.com"),
        CNAMEPattern(suffix=".jcloudimg.com", source="https://beian.miit.gov.cn/", is_leaf=True),
        CNAMEPattern(suffix=".jcloudimg.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jcloudlb.com", source="https://beian.miit.gov.cn/", is_leaf=True),
        CNAMEPattern(suffix=".jd-eit.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jd.shop", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdn.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdn.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdn.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdn.tech", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdndns.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdndns.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdndns.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdndns.tech", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdngslb.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdngslb.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdngslb.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdnops.cn", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud-scdnops.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloud.com", source="https://beian.miit.gov.cn/", is_leaf=True),
        CNAMEPattern(suffix=".jdcloudlive.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdcloudstatus.net", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".jdtxihe.com", source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix=".qianxun.com", source="https://beian.miit.gov.cn/", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["jingdong"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="_cdnautover",
            pattern=r"amNsb3Vk[0-9a-zA-Z]+[=]{0,2}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
