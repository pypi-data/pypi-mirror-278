import glob
import importlib
import os

from cdnmon.model.cdn import CommonCDN


def CDN(name: str) -> CommonCDN:
    module_name = f"cdnmon.model.cdn.{name.replace('-', '_')}"
    module = importlib.import_module(module_name)
    return module.CDN


cdns = []
glob_pattern = os.path.join(os.path.dirname(__file__), "model", "cdn", "*.py")
for path in glob.glob(glob_pattern):
    cdn_name, _ = os.path.splitext(os.path.basename(path))
    black_list = ["__init__"]
    if cdn_name not in black_list:
        cdns.append(CDN(cdn_name))
cdns = sorted(cdns, key=lambda cdn: cdn.name)

__all__ = ["CDN", "cdns"]
