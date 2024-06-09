from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="lumen",
    asn_patterns=["lumen"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # www.bellacanvas.com.    0       IN      CNAME   www.bellacanvas.com.c.section.io.
        # www.bellacanvas.com.c.section.io. 0 IN  A       45.154.183.126
        CNAMEPattern(
            suffix=".c.section.io",
            source="https://www.lumen.com/help/en-us/cdn/application-delivery-solutions/set-up-your-domain/set-up-dns.html",
            is_root=True,
            is_leaf=True,
        ),
        CNAMEPattern(
            suffix=".e.ns1.sectionedge.com",
            is_root=False,
            is_leaf=False,
        ),
        # ;; ANSWER SECTION:
        # tsjybcd.com.            0       IN      CNAME   tsjybcd.com.c.section.io.
        # tsjybcd.com.c.section.io. 0     IN      CNAME   dp4dc74tninedmfkv6humrksrmlqidfm.e.ns1.sectionedge.com.
        # dp4dc74tninedmfkv6humrksrmlqidfm.e.ns1.sectionedge.com. 0 IN CNAME lmn-lax-k1.ep.section.io.
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.135
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.45
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.132
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.42
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.37
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.38
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.44
        # lmn-lax-k1.ep.section.io. 0     IN      A       207.120.32.39
        CNAMEPattern(
            suffix=".ep.section.io",
            is_root=False,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(["lumen"]),
)
