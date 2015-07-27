from time import time
from .status import ExitStatus


class TestRunner(object):
    """docstring for TestRunner"""
    def __init__(self, tests, formatter):
        super(TestRunner, self).__init__()
        self.tests = tests
        self.formatter = formatter
        self.tests_results = []
        self.stats = dict(successes=0,
                          failures=0,
                          errors=0,
                          percentage=0,
                          tests=len(tests)
                          )

    def launch(self):
        self.stats['starttime'] = time()
        self.formatter.started(self.stats)
        self.run_tests()
        self.stats['endtime'] = time()
        self.stats['elapsed'] = self.stats['endtime'] - self.stats['starttime']
        self.stats['success'] = self.stats['tests'] - (self.stats['failures'] +
                                                       self.stats['errors'])
        if self.stats['tests'] > 0:
            ratio = self.stats['success'] / self.stats['tests']
            self.stats['percentage'] = ratio * 100
        self.formatter.ended(self.tests_results, self.stats)
        return self.stats['failures']

    def run_tests(self):
        for test in self.tests:
            result = test.run()
            self.formatter.ran(result, self.stats)
            if result.status is ExitStatus.OK:
                continue
            elif result.status in (
                ExitStatus.killed,
                ExitStatus.timeout,
                ExitStatus.noexec
            ):
                self.stats['failures'] += 1
            else:
                self.stats['errors'] += 1
