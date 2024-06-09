from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="edgio",
    asn_patterns=["edgio"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # www.sigmalive.com.      0       IN      CNAME   47d1362e-ac5a-448d-a673-253e6e52c412.glb.edgio.net.
        # 47d1362e-ac5a-448d-a673-253e6e52c412.glb.edgio.net. 3600 IN CNAME tp01.map.edgio.net.
        # tp01.map.edgio.net.     0       IN      A       152.199.6.208
        CNAMEPattern(suffix=".glb.edgio.net", is_root=True, is_leaf=False),
        CNAMEPattern(suffix=".map.edgio.net", is_root=False, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["edgio"]),
)
