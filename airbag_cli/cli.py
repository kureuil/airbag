class CliFormatter(object):
    def __init__(self):
        super(CliFormatter, self).__init__()

    def batch(self, tests_results, tests_stats):
        self.started(tests_stats)
        for result in tests_results:
            self.ran(result, tests_stats)
        self.ended(tests_results, tests_stats)

    def started(self, tests_stats):
        print(tests_stats)

    def ran(self, test_result, tests_stats):
        print(test_result)

    def ended(self, tests_results, tests_stats):
        print(
            'Ran {0} tests in {1:.1f} seconds.'.format(
                tests_stats['tests'], tests_stats['elapsed']
            )
        )
        print(
            '[{0:.0f}%] Success: {1} | Errors: {3} | Failures: {2}'.format(
                tests_stats['percentage'],
                tests_stats['success'],
                tests_stats['failures'],
                tests_stats['errors']
            )
        )

    def get_type():
        return 'cli'

