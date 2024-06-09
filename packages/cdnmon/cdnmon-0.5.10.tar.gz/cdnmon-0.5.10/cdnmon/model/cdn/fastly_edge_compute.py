from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn.fastly import FastlyCIDR

CDN = CommonCDN(
    name="fastly-edge-compute",
    asn_patterns=["fastly"],
    cname_suffixes=[
        CNAMEPattern(suffix=".edgecompute.app"),
    ],
    cidr=FastlyCIDR(),
)
