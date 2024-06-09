## Introduction

This project provides IP range data of multiple CDN vendors via a Python package named `cdnmon`.

## Installation

```
pip install -i https://pypi.org/simple/ cdnmon
```

## Usage


```python
from cdnmon import CDN

# Get a CDN by name
cloudflare = CDN("cloudflare")

# Get the IP ranges of a specific CDN
cloudflare.ipv4_prefixes()
cloudflare.ipv6_prefixes()

# Get an example subscriber domain of the given CDN
cloudflare.subscribers()
```

## TODO

- [ ] Support downloading ingress / egress nodes list
- [ ] Add `unchanged_since` in `index.html`
- [ ] Change `updated_at` in `index.html`
- [ ] Add example code in `index.html`
- [x] Add type annotations

## FAQ

### How to obtain an access token?

Please contact <wangyihanger@gmail.com>.
