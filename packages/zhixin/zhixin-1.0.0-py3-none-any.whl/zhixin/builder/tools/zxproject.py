from zhixin.compat import MISSING
from zhixin.project.config import ProjectConfig


def GetProjectConfig(env):
    return ProjectConfig.get_instance(env["PROJECT_CONFIG"])


def GetProjectOptions(env, as_dict=False):
    return env.GetProjectConfig().items(env=env["ZXENV"], as_dict=as_dict)


def GetProjectOption(env, option, default=MISSING):
    return env.GetProjectConfig().get("env:" + env["ZXENV"], option, default)


def LoadProjectOptions(env):
    config = env.GetProjectConfig()
    section = "env:" + env["ZXENV"]
    for option in config.options(section):
        option_meta = config.find_option_meta(section, option)
        if (
            not option_meta
            or not option_meta.buildenvvar
            or option_meta.buildenvvar in env
        ):
            continue
        env[option_meta.buildenvvar] = config.get(section, option)


def exists(_):
    return True


def generate(env):
    env.AddMethod(GetProjectConfig)
    env.AddMethod(GetProjectOptions)
    env.AddMethod(GetProjectOption)
    env.AddMethod(LoadProjectOptions)
    return env
