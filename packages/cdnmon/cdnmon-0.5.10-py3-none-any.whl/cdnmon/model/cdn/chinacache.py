from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="chinacache",
    asn_patterns=["chinacache"],
    cname_suffixes=[
        # 北京蓝汛通信技术有限责任公司
        CNAMEPattern(suffix=".ccgslb.com"),
        CNAMEPattern(suffix=".lxcvc.com"),
        # ;; ANSWER SECTION:
        # ts1.cn.mm.bing.net.     0       IN      CNAME   ts1.cn.mm.bing.chinacache.net.
        # ts1.cn.mm.bing.chinacache.net. 0 IN     CNAME   ts1.cn.mm.bing.net.bscedge.com.
        # ts1.cn.mm.bing.net.bscedge.com. 0 IN    CNAME   zmxmsn.v.bscedge.com.
        # zmxmsn.v.bscedge.com.   0       IN      CNAME   msnzlxxglobal.v.bscedge.com.
        # msnzlxxglobal.v.bscedge.com. 0  IN      A       4.79.219.67
        # msnzlxxglobal.v.bscedge.com. 0  IN      A       4.79.219.74
        # msnzlxxglobal.v.bscedge.com. 0  IN      A       4.79.219.72
        CNAMEPattern(suffix=".chinacache.net"),
    ],
    cidr=BGPViewCIDR(["chinacache"]),
    homepage="http://chinacache.com/",
    companies=["北京蓝汛通信技术有限责任公司"],
)
