from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="frontdoor",
    asn_patterns=["frontdoor", "azure", "microsoft"],
    cname_suffixes=[
        # ;; ANSWER SECTION:
        # www.fmsc.org.           0       IN      CNAME   fmsc-frontdoor-sc10.azurefd.net.
        # fmsc-frontdoor-sc10.azurefd.net. 0 IN   CNAME   azurefd-t-prod.trafficmanager.net.
        # azurefd-t-prod.trafficmanager.net. 0 IN CNAME   shed.dual-low.s-part-0041.t-0009.t-msedge.net.
        # shed.dual-low.s-part-0041.t-0009.t-msedge.net. 0 IN CNAME s-part-0041.t-0009.t-msedge.net.
        # s-part-0041.t-0009.t-msedge.net. 0 IN   A       13.107.246.69
        CNAMEPattern(suffix=".azureedge.net", pattern=r"${name}.azureedge.net", is_leaf=True),
        CNAMEPattern(suffix=".azurefd.net", pattern=r"${name}.azurefd.net", is_root=True, is_leaf=False),
        CNAMEPattern(suffix=".azurewebsites.net", pattern=r"${name}.azurewebsites.net", is_root=False, is_leaf=True),
        # ;; ANSWER SECTION:
        # www.stateofflorida.com. 0       IN      CNAME   black-stone-001cc220f.5.azurestaticapps.net.
        # black-stone-001cc220f.5.azurestaticapps.net. 0 IN CNAME azurestaticapps5.trafficmanager.net.
        # azurestaticapps5.trafficmanager.net. 0 IN CNAME msha-slice-5-wus2-1.msha-slice-5-wus2-1-ase.p.azurewebsites.net.
        # msha-slice-5-wus2-1.msha-slice-5-wus2-1-ase.p.azurewebsites.net. 0 IN CNAME waws-prod-mwh-5a9d2a3f.sip.p.azurewebsites.windows.net.
        # waws-prod-mwh-5a9d2a3f.sip.p.azurewebsites.windows.net. 0 IN A 20.69.151.16
        CNAMEPattern(suffix=".azurestaticapps.net"),
        CNAMEPattern(suffix=".azurewebsites.windows.net", is_root=False, is_leaf=True),
        # ;; ANSWER SECTION:
        # portal.office.com.      0       IN      CNAME   admin-portal.office.com.
        # admin-portal.office.com. 0      IN      CNAME   portal-office365-com.b-0004.b-msedge.net.
        # portal-office365-com.b-0004.b-msedge.net. 0 IN CNAME b-0004.b-msedge.net.
        # b-0004.b-msedge.net.    0       IN      A       13.107.6.156
        CNAMEPattern(suffix=".b-msedge.net", is_root=False, is_leaf=True),
        # ;; ANSWER SECTION:
        # pkgs.dev.azure.com.     0       IN      CNAME   star-dev-azure-com.l-0011.l-msedge.net.
        # star-dev-azure-com.l-0011.l-msedge.net. 0 IN CNAME l-0011.l-msedge.net.
        # l-0011.l-msedge.net.    0       IN      A       13.107.42.20
        CNAMEPattern(suffix=".l-msedge.net", is_root=True, is_leaf=True),
        # ;; ANSWER SECTION:
        # pacehr.techmahindra.com. 0      IN      CNAME   pacehr-techmahindra.msappproxy.net.
        # pacehr-techmahindra.msappproxy.net. 0 IN CNAME  edf442f5-b994-4c86-a131-b42b03a16c95.tenant.runtime.msappproxy.net.
        # edf442f5-b994-4c86-a131-b42b03a16c95.tenant.runtime.msappproxy.net. 0 IN CNAME cwap-ind1-runtime.routing.msappproxy.net.
        # cwap-ind1-runtime.routing.msappproxy.net. 0 IN CNAME ind.proxy-1.appproxy.msidentity.com.
        # ind.proxy-1.appproxy.msidentity.com. 0 IN CNAME www.tm.ind.proxy-1.appproxy.trafficmanager.net.
        # www.tm.ind.proxy-1.appproxy.trafficmanager.net. 0 IN CNAME proxy-appproxy-ins-ma1p-1.msappproxy.net.
        # proxy-appproxy-ins-ma1p-1.msappproxy.net. 0 IN A 20.44.48.98
        CNAMEPattern(suffix=".msappproxy.net", is_root=True, is_leaf=True),
        # ;; ANSWER SECTION:
        # eastus1-mediap.svc.ms.  0       IN      CNAME   dual-spo-0005.spo-msedge.net.
        # dual-spo-0005.spo-msedge.net. 0 IN      A       13.107.136.10
        # dual-spo-0005.spo-msedge.net. 0 IN      A       13.107.138.10
        CNAMEPattern(suffix=".spo-msedge.net", is_root=True, is_leaf=True),
        CNAMEPattern(suffix=".t-msedge.net", is_root=False, is_leaf=True),
        # ;; ANSWER SECTION:
        # cosmic-southafricanorth-ns-eedcdd93b000.trafficmanager.net. 10 IN A 52.123.151.63
        CNAMEPattern(suffix=".trafficmanager.net", is_root=False, is_leaf=True),
    ],
    cidr=BGPViewCIDR(["frontdoor", "azure", "microsoft"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="_dnsauth",
            pattern=r"[0-9a-z]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
