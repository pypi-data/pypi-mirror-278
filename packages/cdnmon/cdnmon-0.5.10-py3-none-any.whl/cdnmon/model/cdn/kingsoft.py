from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="kingsoft",
    asn_patterns=["kingsoft", "ksyun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".download.ks-cdn.com", pattern=r"${domain}.download.ks-cdn.com", is_root=True),
        CNAMEPattern(suffix=".ksyuncdn.com", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["kingsoft", "ksyun"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="ksy-cdnauth",
            pattern=r"[0-9a-f]{32}",
        ),
        http=HTTPOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            path="/ksy-cdnauth.html",
            pattern=r"[0-9a-f]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
