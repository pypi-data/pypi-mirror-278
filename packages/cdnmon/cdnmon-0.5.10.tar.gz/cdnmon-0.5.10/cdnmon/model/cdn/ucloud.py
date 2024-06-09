from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="ucloud",
    asn_patterns=["ucloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ucloud.com.cn", pattern=r"${domain}.ucloud.com.cn", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".ucloudnaming.cn", pattern=r"${domain}.ucloudnaming.cn"),
        CNAMEPattern(suffix=".ucloudnaming.info", pattern=r"${domain}.ucloudnaming.info", is_leaf=True),
        CNAMEPattern(suffix=".ugslb.net", pattern=r"${domain}.ugslb.net", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["ucloud"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
