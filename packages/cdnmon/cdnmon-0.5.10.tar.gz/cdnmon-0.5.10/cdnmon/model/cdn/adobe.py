from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="adobe",
    asn_patterns=["adobe"],
    cname_suffixes=[
        CNAMEPattern(
            suffix="cdn.adobeaemcloud.com",
            source="https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/custom-domain-names/configure-dns-settings",
            # ;; ANSWER SECTION:
            # www.otempo.com.br.      10      IN      CNAME   cdn.adobeaemcloud.com.
            # cdn.adobeaemcloud.com.  10      IN      CNAME   adobe-aem.map.fastly.net.
            # adobe-aem.map.fastly.net. 10    IN      A       151.101.111.10
            is_root=True,
            is_leaf=False,
        ),
    ],
    cidr=BGPViewCIDR(["adobe"]),
)
