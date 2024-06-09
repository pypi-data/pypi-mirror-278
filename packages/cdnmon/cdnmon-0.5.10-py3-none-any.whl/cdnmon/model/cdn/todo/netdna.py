# *.netdna-cdn.com
# *.netdna-ssl.com
# *.netdna.com
from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="netdna",
    asn_patterns=["netdna"],
    cname_suffixes=[
        CNAMEPattern(suffix=".netdna-cdn.com", source="https://github.com/EdOverflow/can-i-take-over-xyz/issues/94"),
    ],
    cidr=BGPViewCIDR(["netdna"]),
)
