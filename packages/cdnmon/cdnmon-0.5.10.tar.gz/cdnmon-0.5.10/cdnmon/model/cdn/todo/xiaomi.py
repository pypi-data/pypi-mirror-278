from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="xiaomi",
    asn_patterns=["xiaomi"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # appstore.cdn.pandora.xiaomi.com. 0 IN   CNAME   appstore.cdn.pandora.c.mgslb.com.
        # appstore.cdn.pandora.c.mgslb.com. 0 IN  CNAME   appstore.cdn.pandora.xiaomi.com.w.alikunlun.com.
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.234
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.231
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.229
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.227
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.232
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.228
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.233
        # appstore.cdn.pandora.xiaomi.com.w.alikunlun.com. 0 IN A 121.194.7.230
        # ;; ANSWER SECTION:
        # gimg.cdn.pandora.xiaomi.com. 0  IN      CNAME   gimg.cdn.pandora.c.mgslb.com.
        # gimg.cdn.pandora.c.mgslb.com. 0 IN      CNAME   gimg.cdn.pandora.xiaomi.com.download.ks-cdn.com.
        # gimg.cdn.pandora.xiaomi.com.download.ks-cdn.com. 0 IN CNAME k1.gslb.ksyuncdn.com.
        # k1.gslb.ksyuncdn.com.   0       IN      A       61.170.102.10
        # k1.gslb.ksyuncdn.com.   0       IN      A       183.61.168.3
        # k1.gslb.ksyuncdn.com.   0       IN      A       183.131.56.3
        # k1.gslb.ksyuncdn.com.   0       IN      A       183.131.40.7
        # k1.gslb.ksyuncdn.com.   0       IN      A       113.16.211.1
        # k1.gslb.ksyuncdn.com.   0       IN      A       61.240.218.6
        CNAMEPattern(suffix=".mgslb.com", pattern=r"${domain}.mgslb.com", is_root=True, is_leaf=False),
    ],
    cidr=BGPViewCIDR(["xiaomi"]),
)
