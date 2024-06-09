from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="iverycloud",
    asn_patterns=["iverycloud"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # pc6.com.                0       IN      CNAME   pc6.com.rgslb.cn.
        # pc6.com.rgslb.cn.       0       IN      CNAME   pc6.com.ctadns.cn.
        # pc6.com.ctadns.cn.      0       IN      A       183.136.140.27
        # pc6.com.ctadns.cn.      0       IN      A       183.136.140.24
        # pc6.com.ctadns.cn.      0       IN      A       115.231.173.57
        # pc6.com.ctadns.cn.      0       IN      A       115.231.173.59
        # pc6.com.ctadns.cn.      0       IN      A       115.231.173.58
        # pc6.com.ctadns.cn.      0       IN      A       183.136.140.25
        # pc6.com.ctadns.cn.      0       IN      A       183.136.140.26
        # pc6.com.ctadns.cn.      0       IN      A       115.231.173.56
        CNAMEPattern(suffix=".rgslb.cn", pattern=r"${domain}.rgslb.cn", is_root=True, is_leaf=False),
    ],
    cidr=BGPViewCIDR(["iverycloud"]),
    homepage="https://www.iverycloud.com/",
    companies=["江苏睿鸿网络技术股份有限公司"],
)
