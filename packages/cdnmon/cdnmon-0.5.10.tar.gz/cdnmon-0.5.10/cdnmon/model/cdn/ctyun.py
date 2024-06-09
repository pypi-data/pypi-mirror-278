from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="ctyun",
    asn_patterns=["ctyun", "chinanet"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # pc6.com.                334     IN      CNAME   pc6.com.rgslb.cn.
        # pc6.com.rgslb.cn.       334     IN      CNAME   pc6.com.ctadns.cn.
        # pc6.com.ctadns.cn.      334     IN      A       115.231.173.56
        # pc6.com.ctadns.cn.      334     IN      A       183.136.140.26
        # pc6.com.ctadns.cn.      334     IN      A       183.136.140.25
        # pc6.com.ctadns.cn.      334     IN      A       115.231.173.58
        # pc6.com.ctadns.cn.      334     IN      A       115.231.173.59
        # pc6.com.ctadns.cn.      334     IN      A       115.231.173.57
        # pc6.com.ctadns.cn.      334     IN      A       183.136.140.24
        # pc6.com.ctadns.cn.      334     IN      A       183.136.140.27
        CNAMEPattern(suffix=".ctadns.cn", pattern=r"${domain}.ctadns.cn", is_leaf=True),
        # ;; ANSWER SECTION:
        # mxrb.cn.                0       IN      CNAME   mxrb.cn.ctacdn.cn.
        # mxrb.cn.ctacdn.cn.      0       IN      A       218.67.91.81
        # mxrb.cn.ctacdn.cn.      0       IN      A       106.126.4.84
        CNAMEPattern(suffix=".ctacdn.cn", pattern=r"${domain}.ctacdn.cn", is_root=True, is_leaf=True),
        # ;; ANSWER SECTION:
        # d90.gdl.netease.com.ctlcdn.cn. 592 IN   A       125.77.181.190
        # d90.gdl.netease.com.ctlcdn.cn. 592 IN   A       125.77.181.191
        # d90.gdl.netease.com.ctlcdn.cn. 592 IN   A       125.77.181.192
        CNAMEPattern(suffix=".ctlcdn.cn", pattern=r"${domain}.ctlcdn.cn", is_root=True, is_leaf=True),
        # ;; ANSWER SECTION:
        # storedl5.heytapdownload.com. 0  IN      CNAME   storedl5.heytapdownload.com.ctzcdn.cn.
        # storedl5.heytapdownload.com.ctzcdn.cn. 0 IN A   119.96.5.59
        # storedl5.heytapdownload.com.ctzcdn.cn. 0 IN A   119.96.5.56
        # storedl5.heytapdownload.com.ctzcdn.cn. 0 IN A   119.96.5.58
        # storedl5.heytapdownload.com.ctzcdn.cn. 0 IN A   119.96.5.57
        CNAMEPattern(suffix=".ctzcdn.cn", pattern=r"${domain}.ctzcdn.cn", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".ctyunwaf2.cn"),
        CNAMEPattern(suffix=".ynjtyiptv.cn"),
        CNAMEPattern(suffix=".ahctyiptv.cn"),
        CNAMEPattern(suffix=".ctgcdn.com"),
        CNAMEPattern(suffix=".bjctyiptv.cn"),
        CNAMEPattern(suffix=".shctyiptv.cn"),
        CNAMEPattern(suffix=".jsctyiptv.cn"),
        CNAMEPattern(suffix=".ctydoh.cn"),
        CNAMEPattern(suffix=".fjctyiptv.cn"),
        CNAMEPattern(suffix=".ctfincloud.cn"),
        CNAMEPattern(suffix=".ctyuninner.com"),
        CNAMEPattern(suffix=".ctecdn.cn"),
        CNAMEPattern(suffix=".ctrender.com"),
        CNAMEPattern(suffix=".ctcdnov.com"),
        CNAMEPattern(suffix=".ctyiptv.cn"),
        CNAMEPattern(suffix=".ctcdnov.net"),
        CNAMEPattern(suffix=".ctyunmds.cn"),
        CNAMEPattern(suffix=".ctcdn.com.cn"),
        CNAMEPattern(suffix=".ctyun.com.cn"),
        CNAMEPattern(suffix=".ctdns.com.cn"),
        CNAMEPattern(suffix=".ctxcdn.net"),
        CNAMEPattern(suffix=".ctdns.cn"),
        CNAMEPattern(suffix=".cthcdn.com"),
        CNAMEPattern(suffix=".ctxcdn.cn"),
        CNAMEPattern(suffix=".ctycdn.com"),
        CNAMEPattern(suffix=".ctyun.store"),
        CNAMEPattern(suffix=".ctcdn.com"),
        CNAMEPattern(suffix=".cthcdn.cn"),
        CNAMEPattern(suffix=".ctyunxs.cn"),
        CNAMEPattern(suffix=".cthcdn.net"),
        CNAMEPattern(suffix=".edgecloudx.cn"),
        CNAMEPattern(suffix=".ctzcdn.com"),
        CNAMEPattern(suffix=".ctdcdn.com"),
        CNAMEPattern(suffix=".ctycdn.net.cn"),
        CNAMEPattern(suffix=".ctlcdn.net"),
        CNAMEPattern(suffix=".ctxcdn.com"),
        CNAMEPattern(suffix=".ctycdn.cn"),
        CNAMEPattern(suffix=".ctdns.net"),
        CNAMEPattern(suffix=".ctcdn.cn"),
        CNAMEPattern(suffix=".ctlcdn.com"),
        CNAMEPattern(suffix=".ctmcdn.cn"),
        CNAMEPattern(suffix=".ctyunapi.cn"),
        CNAMEPattern(suffix=".ctbcdn.com"),
        CNAMEPattern(suffix=".ctycdn.net"),
        CNAMEPattern(suffix=".ctyun.cn"),
        CNAMEPattern(suffix=".ctyuncdn.cn"),
    ],
    cidr=BGPViewCIDR(["ctyun", "chinanet"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="dnsverify",
            pattern=r"[0-9]{14}[0-9a-f]{50}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
    homepage="https://www.ctyun.cn/",
    companies=["天翼云科技有限公司"],
)
