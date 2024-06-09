from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="limelight",
    asn_patterns=["limelight"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # oqesn.np.dl.playstation.net. 0  IN      CNAME   l02.cdn.update.playstation.net.
        # l02.cdn.update.playstation.net. 0 IN    CNAME   sonycoment.vo.llnwd.net.
        # sonycoment.vo.llnwd.net. 0      IN      A       68.142.107.1
        # sonycoment.vo.llnwd.net. 0      IN      A       68.142.107.129
        CNAMEPattern(suffix=".llnwd.net", is_root=True, is_leaf=True, example="oqesn.np.dl.playstation.net"),
        # ;; ANSWER SECTION:
        # home.bt.com.            0       IN      CNAME   btgrpsec-dd.lldns.net.
        # btgrpsec-dd.lldns.net.  0       IN      CNAME   btgroup-1.s.llnwi.net.
        # btgroup-1.s.llnwi.net.  0       IN      A       68.142.107.88
        CNAMEPattern(suffix=".llnwi.net", is_root=False, is_leaf=True, example="home.bt.com"),
        # ;; ANSWER SECTION:
        # kms.samsfmm.cust.lldns.net. 0   IN      A       69.28.162.131
        CNAMEPattern(suffix=".lldns.net", is_root=True, is_leaf=True, example="home.bt.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["limelight"]),
)
