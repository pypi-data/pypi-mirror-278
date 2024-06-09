from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="netlify",
    asn_patterns=["netlify"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".netlify.app",
            source="https://www.netlify.com/blog/2020/03/26/how-to-set-up-netlify-dns-custom-domains-cname-and-a-records/",
            is_root=True,
            is_leaf=True,
        ),
        CNAMEPattern(
            suffix=".netlify.com",
            source="https://docs.netlify.com/domains-https/custom-domains/configure-external-dns/",
            is_root=True,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["netlify"]),
)
