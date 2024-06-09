from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="salesforce",
    asn_patterns=["salesforce"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".live.siteforce.com",
            source="https://help.salesforce.com/s/articleView?id=sf.siteforce_domains.htm&type=5",
            is_root=True,
            is_leaf=False,
        ),
        # ;; ANSWER SECTION:
        # support.yahoo-net.jp.   0       IN      CNAME   support.yahoo-net.jp.00d100000002huaeaa.live.siteforce.com.
        # support.yahoo-net.jp.00d100000002huaeaa.live.siteforce.com. 0 IN CNAME 1p.edge2.salesforce.com.
        # 1p.edge2.salesforce.com. 0      IN      CNAME   phoenix-1p.edge2.salesforce.com.
        # phoenix-1p.edge2.salesforce.com. 0 IN   CNAME   ph2.edge2.salesforce.com.
        # ph2.edge2.salesforce.com. 0     IN      A       13.110.52.10
        # ph2.edge2.salesforce.com. 0     IN      A       13.110.52.8
        # ph2.edge2.salesforce.com. 0     IN      A       13.110.52.11
        CNAMEPattern(
            suffix=".edge2.salesforce.com",
            source="https://help.salesforce.com/s/articleView?id=sf.siteforce_domains.htm&type=5",
            is_root=False,
            is_leaf=True,
        ),
        CNAMEPattern(
            suffix=".r.salesforceliveagent.com",
            source="https://help.salesforce.com/s/articleView?id=sf.siteforce_domains.htm&type=5",
            is_root=False,
            is_leaf=True,
        ),
    ],
    cidr=BGPViewCIDR(query_term_list=["salesforce"]),
)
