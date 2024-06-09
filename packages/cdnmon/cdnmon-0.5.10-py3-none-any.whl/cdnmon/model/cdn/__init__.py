import datetime
import functools
import glob
import ipaddress
import os
import sys
import tempfile
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Generator
from typing import List

import humanize
import requests
import yaml
from loguru import logger

from cdnmon.util import bgpview
from cdnmon.util import db
from cdnmon.util.cidr import deduplicate_networks

logger.remove()
logger.add(sys.stderr, level="INFO")


class ETL:
    def extract(self):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data):
        raise NotImplementedError


class CIDR(ETL):
    def ipv4_prefixes(self) -> List[str]:
        return self.transform(self.extract())["ipv4_prefixes"]

    def ipv6_prefixes(self) -> List[str]:
        return self.transform(self.extract())["ipv6_prefixes"]

    @functools.lru_cache(maxsize=None)
    def http_get(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36 "
        }
        response = requests.get(url, headers=headers)
        logger.info(
            f"{response.status_code} {response.reason} | GET {url}  ({humanize.naturalsize(len(response.content))} Bytes)"
        )
        return response


class BGPViewCIDR(CIDR):
    def __init__(self, query_term_list: List[str] = []):
        self.query_term_list = query_term_list
        self.bgpview_client = bgpview.BGPViewClient()

    def ipv4_prefixes(self) -> List[str]:
        ipv4_networks = []
        for query_term in self.query_term_list:
            data = self.bgpview_client.search(query_term)
            for item in data["data"]["ipv4_prefixes"]:
                ipv4_networks.append(str(ipaddress.IPv4Network(item["prefix"], strict=False)))
        return deduplicate_networks(ipv4_networks, filter_version=4)

    def ipv6_prefixes(self) -> List[str]:
        ipv6_networks = []
        for query_term in self.query_term_list:
            data = self.bgpview_client.search(query_term)
            for item in data["data"]["ipv6_prefixes"]:
                ipv6_networks.append(str(ipaddress.IPv6Network(item["prefix"], strict=False)))
        return deduplicate_networks(ipv6_networks, filter_version=6)


class CNAMEType(Enum):
    """
    e.g. For the following DNS result, the CNAMEType defines as follows

        edgekey.net -> ROOT
        akadns.net  -> INTERMEDIATE
        tl88.net    -> LEAF (which means it directly points to an IP address)

    $ dig www.apple.com

    ; <<>> DiG 9.18.24-0ubuntu5-Ubuntu <<>> www.apple.com
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 24731
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 65494
    ;; QUESTION SECTION:
    ;www.apple.com.                 IN      A

    ;; ANSWER SECTION:
    www.apple.com.          0       IN      CNAME   www.apple.com.edgekey.net.
    www.apple.com.edgekey.net. 5050 IN      CNAME   www.apple.com.edgekey.net.globalredir.akadns.net.
    www.apple.com.edgekey.net.globalredir.akadns.net. 0 IN CNAME e6858.e19.s.tl88.net.
    e6858.e19.s.tl88.net.   0       IN      A       106.4.158.58

    ;; Query time: 6 msec
    ;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
    ;; WHEN: Mon May 27 15:48:00 CST 2024
    ;; MSG SIZE  rcvd: 187
    """

    UNKNOWN = "unknown"
    ROOT = "root"
    INTERMEDIATE = "intermediate"
    LEAF = "leaf"

    def __str__(self) -> str:
        return self.value


@dataclass
class CNAMEPattern:
    suffix: str = field(default_factory=str)
    pattern: str = field(default_factory=str)
    source: str = field(default_factory=str)
    example: str = field(default_factory=str)
    is_root: bool | None = field(default=None)
    is_leaf: bool | None = field(default=None)

    def __str__(self) -> str:
        return self.suffix

    def __repr__(self) -> str:
        return self.suffix

    def marshal(self) -> dict:
        top_subscribers = [domain for domain in self.subscribers(max_num=5)]
        top_subscribers.sort()
        result = {
            "suffix": self.suffix,
            "pattern": self.pattern,
            "source": self.source,
            "subscribers": top_subscribers,
        }
        if self.is_root is not None:
            result["is_root"] = self.is_root
        if self.is_leaf is not None:
            result["is_leaf"] = self.is_leaf
        return result

    def subscribers(self, max_num=8) -> Generator[str, None, None]:
        if not os.getenv("MONGODB_URI"):
            logger.warning("MONGODB_URI is not set")
            return

        suffix = self.suffix if self.suffix.endswith(".") else self.suffix + "."
        pattern = f'^{suffix[::-1].replace(".", chr(92)+".")}'
        filter = {
            "task.dns.response.answers.cname_reverse": {"$regex": pattern},
        }
        collection = db.get_mongo_collection("kepler", "dns")
        cache = set()
        for item in collection.find(filter).batch_size(1):
            if len(cache) >= max_num:
                break
            qname = item["task"]["qname"]
            if qname not in cache:
                logger.warning("{} | {}", qname, self.suffix)
                yield qname
                cache.add(qname)
        return


class DomainOwnershipVerficationStatus(Enum):
    REQUIRED = "required"
    NOT_REQUIRED = "not_required"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value


@dataclass
class DomainOwnershipVerification:
    status: DomainOwnershipVerficationStatus = field(default=DomainOwnershipVerficationStatus.UNKNOWN)
    prefix: str = field(default_factory=str)
    pattern: str = field(default_factory=str)

    def __dict__(self) -> dict:
        result = {"status": str(self.status)}
        if self.status == DomainOwnershipVerficationStatus.REQUIRED:
            result["prefix"] = self.prefix
            result["pattern"] = self.pattern
        return result


@dataclass
class HTTPOwnershipVerification:
    status: DomainOwnershipVerficationStatus = field(default=DomainOwnershipVerficationStatus.UNKNOWN)
    path: str = field(default_factory=str)
    pattern: str = field(default_factory=str)

    def __dict__(self) -> dict:
        result = {"status": str(self.status)}
        if self.status == DomainOwnershipVerficationStatus.REQUIRED:
            result["path"] = self.path
            result["pattern"] = self.pattern
        return result


@dataclass
class OwnershipVerification:
    txt: DomainOwnershipVerification = field(default_factory=DomainOwnershipVerification)
    http: HTTPOwnershipVerification = field(default_factory=HTTPOwnershipVerification)

    def __dict__(self) -> dict:
        result = {}
        if self.txt.status != DomainOwnershipVerficationStatus.UNKNOWN:
            result["txt"] = self.txt.__dict__()
        if self.http.status != DomainOwnershipVerficationStatus.UNKNOWN:
            result["http"] = self.http.__dict__()
        return result


@dataclass
class CommonCDN:
    name: str = field(default_factory=str)
    asn_patterns: list[str] = field(default_factory=list)
    cname_suffixes: list[CNAMEPattern] = field(default_factory=list)
    cidr: CIDR = field(default_factory=CIDR)
    frontend_ownership_verification: OwnershipVerification = field(default_factory=OwnershipVerification)
    backend_ownership_verification: OwnershipVerification = field(default_factory=OwnershipVerification)
    homepage: str = field(default_factory=str)
    companies: list[str] = field(default_factory=list)

    def ipv4_prefixes(self) -> List[str]:
        return self.cidr.ipv4_prefixes()

    def ipv6_prefixes(self) -> List[str]:
        return self.cidr.ipv6_prefixes()

    def subscribers(self) -> List[str]:
        results = set()
        for cname_suffix in self.cname_suffixes:
            for subscriber in cname_suffix.subscribers():
                results.add(subscriber)
        return list(results)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def dump(self) -> bool:
        path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__),
                    ),
                ),
            ),
            "assets",
            "cdn",
            f"{self.name}.yaml",
        )

        old_content = ""
        if os.path.exists(path):
            with open(path, mode="r", encoding="utf-8") as f:
                old_content = f.read()

        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            temporary_filename = f.name
            yaml.dump(
                {
                    "name": self.name,
                    "asn_patterns": self.asn_patterns,
                    "cname_suffixes": [i.marshal() for i in self.cname_suffixes],
                    "ipv4_prefixes": self.ipv4_prefixes(),
                    "ipv6_prefixes": self.ipv6_prefixes(),
                    "frontend_ownership_verification": self.frontend_ownership_verification.__dict__(),
                    "backend_ownership_verification": self.backend_ownership_verification.__dict__(),
                    "updated_at": datetime.datetime.now().isoformat(),
                },
                f,
            )

        with open(temporary_filename, mode="r", encoding="utf-8") as f:
            new_content = f.read()

        old_lines = [line for line in old_content.splitlines() if not line.startswith("updated_at:")]
        new_lines = [line for line in new_content.splitlines() if not line.startswith("updated_at:")]

        if old_lines != new_lines:
            # move temporary file to the original file
            os.replace(temporary_filename, path)
            return True
        else:
            # remove temporary file
            os.remove(temporary_filename)
            return False


__all__ = []
for path in glob.glob(f"{os.path.dirname(__file__)}/*.py"):
    name, _ = os.path.splitext(os.path.basename(path))
    if name != "__init__":
        __all__.append(name)
