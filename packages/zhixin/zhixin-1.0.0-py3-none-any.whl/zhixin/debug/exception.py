# Copyright (c) 2014-present ZhiXin <contact@zhixin-semi.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zhixin.exception import ZhixinException, UserSideException


class DebugError(ZhixinException):
    pass


class DebugSupportError(DebugError, UserSideException):
    MESSAGE = (
        "Currently, ZhiXin does not support debugging for `{0}`.\n"
        "Please request support at https://github.com/zhixin/"
        "zhixin-core/issues \nor visit -> https://docs.zhixin-semi.com"
        "/page/plus/debugging.html"
    )


class DebugInvalidOptionsError(DebugError, UserSideException):
    pass


class DebugInitError(DebugError, UserSideException):
    pass
