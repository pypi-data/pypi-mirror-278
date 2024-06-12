import os

from zhixin.builder.tools import zxbuild
from zhixin.test.result import TestSuite
from zhixin.test.runners.factory import TestRunnerFactory


def ConfigureTestTarget(env):
    env.Append(
        CPPDEFINES=["UNIT_TEST"],  # deprecated, use ZX_UNIT_TESTING
        ZXTEST_SRC_FILTER=[f"+<*.{ext}>" for ext in zxbuild.SRC_BUILD_EXT],
    )
    env.Prepend(CPPPATH=["$PROJECT_TEST_DIR"])

    if "ZXTEST_RUNNING_NAME" in env:
        test_name = env["ZXTEST_RUNNING_NAME"]
        while True:
            test_name = os.path.dirname(test_name)  # parent dir
            # skip nested tests (user's side issue?)
            if not test_name or os.path.basename(test_name).startswith("test_"):
                break
            env.Prepend(
                ZXTEST_SRC_FILTER=[
                    f"+<{test_name}{os.path.sep}*.{ext}>"
                    for ext in zxbuild.SRC_BUILD_EXT
                ],
                CPPPATH=[os.path.join("$PROJECT_TEST_DIR", test_name)],
            )

        env.Prepend(
            ZXTEST_SRC_FILTER=[f"+<$ZXTEST_RUNNING_NAME{os.path.sep}>"],
            CPPPATH=[os.path.join("$PROJECT_TEST_DIR", "$ZXTEST_RUNNING_NAME")],
        )

    test_runner = TestRunnerFactory.new(
        TestSuite(env["ZXENV"], env.get("ZXTEST_RUNNING_NAME", "*")),
        env.GetProjectConfig(),
    )
    test_runner.configure_build_env(env)


def generate(env):
    env.AddMethod(ConfigureTestTarget)


def exists(_):
    return True
