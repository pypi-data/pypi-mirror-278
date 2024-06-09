from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdnetworks",
    asn_patterns=["cdnetworks"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # apps.samsung.com.       0       IN      CNAME   apps.gw.samsungapps.com.
        # apps.gw.samsungapps.com. 0      IN      CNAME   apps.samsung.com.gslb.cdnetworks.net.
        # apps.samsung.com.gslb.cdnetworks.net. 7200 IN CNAME apps.samsung.com.wtxcdn.com.
        # apps.samsung.com.wtxcdn.com. 0  IN      A       138.113.26.159
        CNAMEPattern(suffix=".gslb.cdnetworks.net", is_root=True, is_leaf=False),
    ],
    cidr=BGPViewCIDR(["cdnetworks"]),
)
