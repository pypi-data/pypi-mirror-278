import platform

from zhixin.compat import PY36, is_proxy_set


def get_core_dependencies():
    return {
        "contrib-zxhome": "~3.4.2",
        "contrib-zxremote": "~1.0.0",
        "tool-scons": "~4.40700.0",
        "tool-cppcheck": "~1.21100.0",
        "tool-clangtidy": "~1.150005.0",
        "tool-pvs-studio": "~7.18.0",
    }


def get_pip_dependencies():
    core = [
        "bottle == 0.12.*",
        "click >=8.0.4, <9",
        "colorama",
        "marshmallow == 3.*",
        "pyelftools >=0.27, <1",
        "pyserial == 3.5.*",  # keep in sync "device/monitor/terminal.py"
        "requests%s == 2.*" % ("[socks]" if is_proxy_set(socks=True) else ""),
        "semantic_version == 2.10.*",
        "tabulate == 0.*",
    ]

    home = [
        # ZX Home requirements
        "ajsonrpc == 1.2.*",
        "starlette >=0.19, <0.38",
        "uvicorn %s" % ("== 0.16.0" if PY36 else ">=0.16, <0.30"),
        "wsproto == 1.*",
    ]

    extra = []

    # issue #4702; Broken "requests/charset_normalizer" on macOS ARM
    if platform.system() == "Darwin" and "arm" in platform.machine().lower():
        extra.append("chardet>=3.0.2,<6")

    # issue 4614: urllib3 v2.0 only supports OpenSSL 1.1.1+
    try:
        import ssl  # pylint: disable=import-outside-toplevel

        if ssl.OPENSSL_VERSION.startswith("OpenSSL ") and ssl.OPENSSL_VERSION_INFO < (
            1,
            1,
            1,
        ):
            extra.append("urllib3<2")
    except ImportError:
        pass

    return core + home + extra
