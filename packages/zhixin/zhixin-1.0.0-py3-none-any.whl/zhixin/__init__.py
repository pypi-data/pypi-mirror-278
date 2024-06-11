VERSION = (1, 0, "0")
__version__ = ".".join([str(s) for s in VERSION])

__title__ = "zhixin"
__description__ = (
    "Your Gateway to Embedded Software Development Excellence. "
    "Unlock the true potential of embedded software development "
    "with ZhiXin's collaborative ecosystem, embracing "
    "declarative principles, test-driven methodologies, and "
    "modern toolchains for unrivaled success."
)
__url__ = "https://zhixin-semi.com"

__author__ = "ZhiXin-Semi"
__email__ = "contact@zhixin-semi.com"

__license__ = "Apache Software License"
__copyright__ = "Copyright 2014-present ZhiXin Semi"

__accounts_api__ = "https://api.accounts.zhixin-semi.com"
__registry_mirror_hosts__ = [
    "registry.zhixin-semi.com",
    "registry.nm1.zhixin-semi.com",
]
__zxremote_endpoint__ = "ssl:host=remote.zhixin-semi.com:port=4413"

__check_internet_hosts__ = [
    "185.199.110.153",  # Github.com
    "88.198.170.159",  # zhixin-semi.com
    "github.com",
] + __registry_mirror_hosts__
