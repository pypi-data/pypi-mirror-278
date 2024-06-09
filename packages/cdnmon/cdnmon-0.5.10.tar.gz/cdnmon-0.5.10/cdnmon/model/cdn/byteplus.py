from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="byteplus",
    asn_patterns=["byteplus", "bytedance"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # m.filesun.com.          300     IN      CNAME   m.filesun.com.bplslb.com.
        # m.filesun.com.bplslb.com. 120   IN      A       169.150.230.131
        # m.filesun.com.bplslb.com. 120   IN      A       169.150.230.129
        # m.filesun.com.bplslb.com. 120   IN      A       169.150.230.130
        CNAMEPattern(
            suffix=".bplslb.com",
            pattern=r"${domain}.bplslb.com",
            source="https://docs.byteplus.com/zh-CN/docs/byteplus-cdn/docs-set-up-cname",
            is_root=True,
            is_leaf=True,
        ),
        CNAMEPattern(
            suffix="ovx-common.bpltm.com",
            pattern=r"ovx-common.bpltm.com",
            is_root=False,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["byteplus", "bytedance"]),
)
