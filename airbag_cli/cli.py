from airbag.status import ExitStatus, ChromeMessage as Chrome


class CliFormatter:
    def __init__(self, message_bag, stream):
        super().__init__()
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
        self.stream.write(
            self.message_bag.get_chrome_str(Chrome.RAN_TEST).format(
                test_result.program,
                test_result.name,
                state
            )
        )
        if test_result.status == ExitStatus.finished:
            for error in test_result.errors:
                self.stream.write(
                   self.message_bag
                        .get_error_str(error['type'])
                        .format(*(error['args'])) + '\n'
                )

    def ended(self, tests_results, tests_stats):
        self.stream.write(
            self.message_bag.get_chrome_str(Chrome.RAN_TESTS).format(
                tests_stats['tests'], tests_stats['elapsed']
            )
        )
        self.stream.write(
            self.message_bag.get_chrome_str(Chrome.TESTS_STATS).format(
                tests_stats['percentage'],
                tests_stats['success'],
                tests_stats['failures'],
                tests_stats['errors']
            )
        )

    @staticmethod
    def get_type():
        return 'cli'
