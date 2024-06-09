from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="alibaba-dcdn",
    asn_patterns=["alibaba", "taobao", "alicloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdngslb.com", pattern=r"${domain}.cdngslb.com", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".m.alikunlun.com", pattern=r"${domain}.m.alikunlun.com", is_leaf=True),
        CNAMEPattern(suffix=".m.alikunlun.net", pattern=r"${domain}.m.alikunlun.net", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunaq.com", pattern=r"${domain}.w.kunlunaq.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunar.com", pattern=r"${domain}.w.kunlunar.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunca.com", pattern=r"${domain}.w.kunlunca.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunluncan.com", pattern=r"${domain}.w.kunluncan.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunea.com", pattern=r"${domain}.w.kunlunea.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlungem.com", pattern=r"${domain}.w.kunlungem.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlungr.com", pattern=r"${domain}.w.kunlungr.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunhuf.com", pattern=r"${domain}.w.kunlunhuf.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunle.com", pattern=r"${domain}.w.kunlunle.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunno.com", pattern=r"${domain}.w.kunlunno.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunpi.com", pattern=r"${domain}.w.kunlunpi.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunsl.com", pattern=r"${domain}.w.kunlunsl.com", is_leaf=True),
        CNAMEPattern(suffix=".w.kunlunso.com", pattern=r"${domain}.w.kunlunso.com", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["alibaba", "taobao", "alicloud"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="verification",
            pattern=r"verify_[0-9a-f]{32}",
        ),
        http=HTTPOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            path="/verification.html",
            pattern=r"verify_[0-9a-f]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
