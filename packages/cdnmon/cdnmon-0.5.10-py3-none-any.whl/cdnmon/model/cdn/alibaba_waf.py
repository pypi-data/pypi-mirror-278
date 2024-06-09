from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="alibaba-waf",
    asn_patterns=["alibaba", "taobao", "alicloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".yundunwaf1.com", pattern=r"${random}.yundunwaf1.com", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".yundunwaf2.com", pattern=r"${random}.yundunwaf2.com", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".yundunwaf3.com", pattern=r"${random}.yundunwaf3.com", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".yundunwaf4.com", pattern=r"${random}.yundunwaf4.com", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".yundunwaf5.com", pattern=r"${random}.yundunwaf5.com", is_root=True, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["alibaba", "taobao", "alicloud"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="wafdnscheck",
            pattern=r"[0-9]{16}-[0-9a-z]{32}",
        )
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
