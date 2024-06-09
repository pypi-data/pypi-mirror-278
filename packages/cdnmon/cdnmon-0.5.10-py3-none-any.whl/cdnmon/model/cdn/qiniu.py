from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="qiniu",
    asn_patterns=["qiniu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".qiniudns.com", pattern=r"${dot2dash-domain}-id[0-9a-z]{5}.qiniudns.com", is_leaf=True),
        CNAMEPattern(suffix=".hiecheimaetu.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".mikubkt.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".mikuhost.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniumiku.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".mikuio.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".mikudns.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".mikuapi.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qnvic.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qnvic.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuvic.cn", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuvic.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuio.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuqcdn.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qnqcdn.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuqcdn.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniup.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qnydns.com", source="https://beian.miit.gov.cn", is_leaf=True),
        CNAMEPattern(suffix=".niuclass.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniukodo.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".everbox.net", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuapp.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniublob.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniuinc.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniu.us", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qnssl.com", source="https://beian.miit.gov.cn"),
        CNAMEPattern(suffix=".qiniudns2.com", source="https://beian.miit.gov.cn"),
    ],
    cidr=BGPViewCIDR(query_term_list=["qiniu"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="verification",
            pattern=r"verify_[0-9a-f]{33}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
