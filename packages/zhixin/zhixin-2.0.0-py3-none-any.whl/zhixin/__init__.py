VERSION = (2, 0, "0")
__version__ = ".".join([str(s) for s in VERSION])

__title__ = "zhixin"
__description__ = (
    "Your Gateway to Embedded Software Development Excellence. "
    "Unlock the true potential of embedded software development "
    "with ZhiXin's collaborative ecosystem, embracing "
    "declarative principles, test-driven methodologies, and "
    "modern toolchains for unrivaled success."
)
__url__ = "https://ZhiXin-Semi.com"

__author__ = "ZhiXin-Semi"
__email__ = "contact@ZhiXin-Semi.com"

__license__ = "Apache Software License"
__copyright__ = "Copyright 2014-present ZhiXin-Semi"

__accounts_api__ = "https://api.accounts.ZhiXin-Semi.com"
__registry_mirror_hosts__ = [
]
__zxremote_endpoint__ = "ssl:host=remote.ZhiXin-Semi.com:port=4413"

__check_internet_hosts__ = [
    "185.199.110.153",  # Github.com
    "github.com",
] + __registry_mirror_hosts__
