from airbag.status import ExitStatus


class CliFormatter(object):
    def __init__(self, message_bag, stream):
        super(CliFormatter, self).__init__()
        self.message_bag = message_bag
        self.stream = stream

    def batch(self, tests_results, tests_stats):
        self.started(tests_stats)
        for result in tests_results:
            self.ran(result, tests_stats)
        self.ended(tests_results, tests_stats)

    def started(self, tests_stats):
        pass

    def ran(self, test_result, tests_stats):
        state = self.message_bag.get_status_str(test_result.status)
        self.stream.write('[{0}]{1}: {2}\n'.format(
            test_result.program,
            test_result.name,
            state
        ))
        if test_result.status == ExitStatus.finished:
            for error in test_result.errors:
                self.stream.write(
                   self.message_bag
                        .get_error_str(error['type'])
                        .format(*(error['args'])) + '\n'
                )

    def ended(self, tests_results, tests_stats):
        self.stream.write(
            'Ran {0} tests in {1:.1f} seconds.\n'.format(
                tests_stats['tests'], tests_stats['elapsed']
            )
        )
        self.stream.write(
            '[{0:.0f}%] Success: {1} | Errors: {3} | Failures: {2}\n'.format(
                tests_stats['percentage'],
                tests_stats['success'],
                tests_stats['failures'],
                tests_stats['errors']
            )
        )

    def get_type():
        return 'cli'
