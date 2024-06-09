from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdn77",
    asn_patterns=["cdn77"],
    cname_suffixes=[
        # web.webpushs.com.       0       IN      CNAME   1317109900.rsc.cdn77.org.
        # 1317109900.rsc.cdn77.org. 0     IN      A       89.187.187.15
        # 1317109900.rsc.cdn77.org. 0     IN      A       143.244.51.207
        # 1317109900.rsc.cdn77.org. 0     IN      A       89.187.187.20
        # 1317109900.rsc.cdn77.org. 0     IN      A       143.244.51.200
        # 1317109900.rsc.cdn77.org. 0     IN      A       89.187.187.11
        # 1317109900.rsc.cdn77.org. 0     IN      A       143.244.51.8
        # 1317109900.rsc.cdn77.org. 0     IN      A       143.244.51.249
        CNAMEPattern(
            suffix=".rsc.cdn77.org",
            source="https://client.cdn77.com/support/knowledgebase/cdn-resource/configuring-cname",
            is_root=True,
            is_leaf=True,
        ),
        CNAMEPattern(suffix=".cdn77.net"),
    ],
    cidr=BGPViewCIDR(["cdn77"]),
)
