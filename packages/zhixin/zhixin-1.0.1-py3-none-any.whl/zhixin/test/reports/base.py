import importlib

from zhixin.test.result import TestResult


class TestReportBase:
    def __init__(self, test_result):
        self.test_result = test_result

    def generate(self, output_path, verbose):
        raise NotImplementedError()


class TestReportFactory:
    @staticmethod
    def new(format, test_result) -> TestReportBase:  # pylint: disable=redefined-builtin
        assert isinstance(test_result, TestResult)
        mod = importlib.import_module(f"zhixin.test.reports.{format}")
        report_cls = getattr(mod, "%sTestReport" % format.lower().capitalize())
        return report_cls(test_result)
