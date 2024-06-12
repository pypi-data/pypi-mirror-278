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

from zhixin import exception
from zhixin.check.tools.clangtidy import ClangtidyCheckTool
from zhixin.check.tools.cppcheck import CppcheckCheckTool
from zhixin.check.tools.pvsstudio import PvsStudioCheckTool


class CheckToolFactory:
    @staticmethod
    def new(tool, project_dir, config, envname, options):
        cls = None
        if tool == "cppcheck":
            cls = CppcheckCheckTool
        elif tool == "clangtidy":
            cls = ClangtidyCheckTool
        elif tool == "pvs-studio":
            cls = PvsStudioCheckTool
        else:
            raise exception.ZhixinException("Unknown check tool `%s`" % tool)
        return cls(project_dir, config, envname, options)
