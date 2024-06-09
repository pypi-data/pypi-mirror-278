from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="baidu",
    asn_patterns=["baidu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".a.bdydns.com", pattern=r"${domain}.a.bdydns.com", is_root=True),
        CNAMEPattern(suffix=".yjs-cdn.com", pattern=r"${domain}.yjs-cdn.com", is_root=True),
        CNAMEPattern(suffix=".yunjiasu-cdn.net", pattern=r"${domain}.yunjiasu-cdn.net", is_root=True),
        CNAMEPattern(suffix="opencdnka.jomodns.com", pattern=r"opencdnka.jomodns.com", is_leaf=True),
        CNAMEPattern(suffix="opencdnkav6.jomodns.com", pattern=r"opencdnkav6.jomodns.com", is_leaf=True),
    ],
    cidr=BGPViewCIDR(["baidu"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="bdy-verify",
            pattern=r"[0-9a-f]{8}-[0-9a-f]{8}",
        ),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
