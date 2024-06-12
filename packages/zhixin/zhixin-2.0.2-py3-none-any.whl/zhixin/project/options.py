# Copyright (c) 2014-present ZhiXin <contact@ZhiXin-Semi.com>
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

# pylint: disable=redefined-builtin, too-many-arguments

import os
from collections import OrderedDict

import click

from zhixin import fs
from zhixin.compat import IS_WINDOWS


class ConfigOption:  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        scope,
        group,
        name,
        description,
        type=str,
        multiple=False,
        sysenvvar=None,
        buildenvvar=None,
        oldnames=None,
        default=None,
        validate=None,
    ):
        self.scope = scope
        self.group = group
        self.name = name
        self.description = description
        self.type = type
        self.multiple = multiple
        self.sysenvvar = sysenvvar
        self.buildenvvar = buildenvvar
        self.oldnames = oldnames
        self.default = default
        self.validate = validate

    def as_dict(self):
        result = dict(
            scope=self.scope,
            group=self.group,
            name=self.name,
            description=self.description,
            type="string",
            multiple=self.multiple,
            sysenvvar=self.sysenvvar,
            default=self.default() if callable(self.default) else self.default,
        )
        if isinstance(self.type, click.ParamType):
            result["type"] = self.type.name
        if isinstance(self.type, (click.IntRange, click.FloatRange)):
            result["min"] = self.type.min
            result["max"] = self.type.max
        if isinstance(self.type, click.Choice):
            result["choices"] = self.type.choices
        return result


def ConfigZhixinOption(*args, **kwargs):
    return ConfigOption("zhixin", *args, **kwargs)


def ConfigEnvOption(*args, **kwargs):
    return ConfigOption("env", *args, **kwargs)


def validate_dir(path):
    if not path:
        return path
    # if not all values expanded, ignore validation
    if "${" in path and "}" in path:
        return path
    if path.startswith("~"):
        path = fs.expanduser(path)
    return os.path.abspath(path)


def get_default_core_dir():
    path = os.path.join(fs.expanduser("~"), ".zhixin")
    if IS_WINDOWS:
        win_core_dir = os.path.splitdrive(path)[0] + "\\.zhixin"
        if os.path.isdir(win_core_dir):
            return win_core_dir
    return path


ProjectOptions = OrderedDict(
    [
        ("%s.%s" % (option.scope, option.name), option)
        for option in [
            #
            # [zhixin]
            #
            ConfigZhixinOption(
                group="generic",
                name="name",
                description="A project name",
                default=lambda: os.path.basename(os.getcwd()),
            ),
            ConfigZhixinOption(
                group="generic",
                name="description",
                description="Describe a project with a short information",
            ),
            ConfigZhixinOption(
                group="generic",
                name="default_envs",
                description=(
                    "Configure a list with environments which ZhiXin should "
                    "process by default"
                ),
                oldnames=["env_default"],
                multiple=True,
                sysenvvar="ZHIXIN_DEFAULT_ENVS",
            ),
            # Dirs
            ConfigZhixinOption(
                group="directory",
                name="build_dir",
                description=(
                    "ZhiXin Build System uses this folder for project environments"
                    " to store compiled object files, static libraries, firmwares, "
                    "and other cached information"
                ),
                sysenvvar="ZHIXIN_BUILD_DIR",
                default=os.path.join("${zhixin.workspace_dir}", "build"),
                validate=validate_dir,
            ),
            ConfigZhixinOption(
                group="directory",
                name="include_dir",
                description=(
                    "A default location for project header files. ZhiXin Build "
                    "System automatically adds this path to CPPPATH scope"
                ),
                multiple=True,
                sysenvvar="ZHIXIN_INCLUDE_DIR",
                default=os.path.join("${PROJECT_DIR}", "include"),
                validate=validate_dir,
            ),
            ConfigZhixinOption(
                group="directory",
                name="src_dir",
                description=(
                    "A default location where ZhiXin Build System looks for the "
                    "project C/C++ source files"
                ),
                multiple=True,
                sysenvvar="ZHIXIN_SRC_DIR",
                default=os.path.join("${PROJECT_DIR}", "src"),
                validate=validate_dir,
            ),
            #
            # [env]
            #
            # Platform
            ConfigEnvOption(
                group="platform",
                name="Device",
                description="A name of development platform",
                type=click.Choice([["Z20K114M", "Z20K116M", "Z20K118M"], ["Z20K144M", "Z20K146M", "Z20K148M"], ["Z20K118N"]]),
            ),
        ]
    ]
)


def get_config_options_schema():
    return [opt.as_dict() for opt in ProjectOptions.values()]
