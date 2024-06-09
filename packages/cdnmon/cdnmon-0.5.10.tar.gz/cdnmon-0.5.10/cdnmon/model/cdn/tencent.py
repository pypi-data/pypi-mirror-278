from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="tencent",
    asn_patterns=["tencent"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdn.dnsv1.com.cn", pattern=r"${domain}.cdn.dnsv1.com.cn"),
        CNAMEPattern(suffix=".cdn.dnsv1.com", pattern=r"${domain}.cdn.dnsv1.com"),
        CNAMEPattern(suffix=".cdn.qcloudcdn.cn", pattern=r"${domain}.cdn.qcloudcdn.cn"),
        CNAMEPattern(suffix=".dsa.dnsv1.com.cn", pattern=r"${domain}.dsa.dnsv1.com.cn"),
        CNAMEPattern(suffix=".dsa.dnsv1.com", pattern=r"${domain}.dsa.dnsv1.com"),
        CNAMEPattern(suffix=".eo.dnse0.com", pattern=r"${domain}.eo.dnse0.com", is_leaf=True),
        CNAMEPattern(suffix=".eo.dnse1.com", pattern=r"${domain}.eo.dnse1.com", is_leaf=True),
        CNAMEPattern(suffix=".eo.dnse2.com", pattern=r"${domain}.eo.dnse2.com", is_leaf=True),
        CNAMEPattern(suffix=".eo.dnse3.com", pattern=r"${domain}.eo.dnse3.com", is_leaf=True),
        CNAMEPattern(suffix=".eo.dnse4.com", pattern=r"${domain}.eo.dnse4.com", is_leaf=True),
        CNAMEPattern(suffix=".eo.dnse5.com", pattern=r"${domain}.eo.dnse5.com", is_leaf=True),
        CNAMEPattern(suffix=".ovscdns.com", pattern=r"${domain}.ovscdns.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv1.com", pattern=r"${random}.slt-dk.sched.tdnsv1.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv2.com", pattern=r"${random}.slt-dk.sched.tdnsv2.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv3.com", pattern=r"${random}.slt-dk.sched.tdnsv3.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv4.com", pattern=r"${random}.slt-dk.sched.tdnsv4.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv5.com", pattern=r"${random}.slt-dk.sched.tdnsv5.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv6.com", pattern=r"${random}.slt-dk.sched.tdnsv6.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv7.com", pattern=r"${random}.slt-dk.sched.tdnsv7.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv8.com", pattern=r"${random}.slt-dk.sched.tdnsv8.com", is_leaf=True),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv9.com", pattern=r"${random}.slt-dk.sched.tdnsv9.com", is_leaf=True),
        CNAMEPattern(suffix=".txlivecdn.com", pattern=r"${domain}.txlivecdn.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["tencent"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="_cdnauth",
            pattern=r"[0-9]{14}[0-9a-f]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
