from concurrent.futures import ThreadPoolExecutor
from time import time
from .status import ExitStatus


class TestRunner:
    """docstring for TestRunner"""
    def __init__(self, tests, formatters, workers=1):
        super().__init__()
        self.tests = tests
        self.workers = workers
        self.formatters = formatters
        self.tests_results = []
        self.stats = dict(successes=0,
                          failures=0,
                          errors=0,
                          percentage=0,
                          tests=len(tests)
                          )

    def launch(self):
        self.stats['starttime'] = time()
        for formatter in self.formatters:
            formatter.started(self.stats)
        self.run_tests()
        self.stats['endtime'] = time()
        self.stats['elapsed'] = self.stats['endtime'] - self.stats['starttime']
        self.stats['success'] = self.stats['tests'] - (self.stats['failures'] +
                                                       self.stats['errors'])
        if self.stats['tests'] > 0:
            ratio = self.stats['success'] / self.stats['tests']
            self.stats['percentage'] = ratio * 100
        for formatter in self.formatters:
            formatter.ended(self.tests_results, self.stats)
        return self.stats['failures']

    def run_tests(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            executor.map(self.run_test, self.tests)

    def run_test(self, test):
        result = test.run()
        for formatter in self.formatters:
            formatter.ran(result, self.stats)
        if result.status is ExitStatus.OK:
            return
        elif result.status in (
            ExitStatus.killed,
            ExitStatus.timeout,
            ExitStatus.noexec
        ):
            self.stats['failures'] += 1
        else:
            self.stats['errors'] += 1