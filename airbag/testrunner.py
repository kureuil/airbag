from time import time
from .status import ExitStatus


class TestRunner(object):
    """docstring for TestRunner"""
    def __init__(self, tests):
        super(TestRunner, self).__init__()
        self.tests = tests

    def launch(self):
        starttime = time()
        failures = 0
        errors = 0
        for test in self.tests:
            status = test.run()
            if status is ExitStatus.ok:
                continue
            elif status in (
                ExitStatus.killed,
                ExitStatus.timeout,
                ExitStatus.noexec
            ):
                failures += 1
            else:
                errors += 1
        tests = len(self.tests)
        success = len(self.tests) - (failures + errors)
        percentage = 0
        if tests > 0:
            percentage = success / tests * 100
        print(
            'Ran {0} tests in {1:.1f} seconds.'.format(
                tests, time() - starttime
            )
        )
        print(
            '[{0:.0f}%] Success: {1} | Errors: {3} | Failures: {2}'.format(
                percentage,
                success,
                failures,
                errors
            )
        )
        return failures
