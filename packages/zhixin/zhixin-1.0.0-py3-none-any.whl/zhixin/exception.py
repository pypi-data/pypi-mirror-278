class ZhixinException(Exception):
    MESSAGE = None

    def __str__(self):  # pragma: no cover
        if self.MESSAGE:
            # pylint: disable=not-an-iterable
            return self.MESSAGE.format(*self.args)

        return super().__str__()


class ReturnErrorCode(ZhixinException):
    MESSAGE = "{0}"


class UserSideException(ZhixinException):
    pass


class AbortedByUser(UserSideException):
    MESSAGE = "Aborted by user"


#
# UDEV Rules
#


class InvalidUdevRules(UserSideException):
    pass


class MissedUdevRules(InvalidUdevRules):
    MESSAGE = (
        "Warning! Please install `99-zhixin-udev.rules`. \nMore details: "
        "https://docs.zhixin-semi.com/en/latest/core/installation/udev-rules.html"
    )


class OutdatedUdevRules(InvalidUdevRules):
    MESSAGE = (
        "Warning! Your `{0}` are outdated. Please update or reinstall them."
        "\nMore details: "
        "https://docs.zhixin-semi.com/en/latest/core/installation/udev-rules.html"
    )


#
# Misc
#


class GetSerialPortsError(ZhixinException):
    MESSAGE = "No implementation for your platform ('{0}') available"


class GetLatestVersionError(ZhixinException):
    MESSAGE = "Can not retrieve the latest ZhiXin version"


class InvalidSettingName(UserSideException):
    MESSAGE = "Invalid setting with the name '{0}'"


class InvalidSettingValue(UserSideException):
    MESSAGE = "Invalid value '{0}' for the setting '{1}'"


class InvalidJSONFile(ValueError, UserSideException):
    MESSAGE = "Could not load broken JSON: {0}"


class CIBuildEnvsEmpty(UserSideException):
    MESSAGE = (
        "Can't find ZhiXin build environments.\n"
        "Please specify `--board` or path to `zhixin.ini` with "
        "predefined environments using `--project-conf` option"
    )


class HomeDirPermissionsError(UserSideException):
    MESSAGE = (
        "The directory `{0}` or its parent directory is not owned by the "
        "current user and ZhiXin can not store configuration data.\n"
        "Please check the permissions and owner of that directory.\n"
        "Otherwise, please remove manually `{0}` directory and ZhiXin "
        "will create new from the current user."
    )


class CygwinEnvDetected(ZhixinException):
    MESSAGE = (
        "ZhiXin does not work within Cygwin environment. "
        "Use native Terminal instead."
    )
