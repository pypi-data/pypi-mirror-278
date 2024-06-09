from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="upyun",
    asn_patterns=["youpai", "upyun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".b0.aicdn.com", pattern=r"[0-9a-f]{12}.b0.aicdn.com", is_root=True),
        CNAMEPattern(suffix="nm.aicdn.com", pattern="nm.aicdn.com", is_leaf=True),
        CNAMEPattern(suffix="vm.ctn.aicdn.com", pattern="vm.ctn.aicdn.com", is_leaf=True),
        CNAMEPattern(suffix="aicdn1.com", pattern="aicdn1.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="aicdn2.com", pattern="aicdn2.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="aicdn3.com", pattern="aicdn3.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="aicdn4.com", pattern="aicdn4.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="aicdn5.com", pattern="aicdn5.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="cdnv1.net", pattern="cdnv1.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="cdnv2.net", pattern="cdnv2.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="cdnv3.net", pattern="cdnv3.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="cdnv4.net", pattern="cdnv4.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="cdnv5.net", pattern="cdnv5.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="oncdp.com", pattern="oncdp.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="sktcdn.com", pattern="sktcdn.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="upai.com", pattern="upai.com", is_leaf=True, source="https://beian.miit.gov.cn/"),
        CNAMEPattern(suffix="upcdn.net", pattern="upcdn.net", is_leaf=True, source="https://beian.miit.gov.cn/"),
    ],
    cidr=BGPViewCIDR(query_term_list=["youpai", "upyun"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="upyun-verify",
            pattern=r"[0-9a-f]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
