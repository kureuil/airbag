from .status import ExitStatus, ChromeMessage as Chrome
from .result import ErrorType


class MessageBag(object):
    def __init__(self):
        super(MessageBag, self).__init__()
        self.status_messages = {}
        self.status_messages[ExitStatus.OK] = 'OK'
        self.status_messages[ExitStatus.finished] = 'KO'
        self.status_messages[ExitStatus.killed] = 'KO'
        self.status_messages[ExitStatus.timeout] = 'KO'
        self.status_messages[ExitStatus.noexec] = 'KO'
        self.errmessages = {}
        self.errmessages[ErrorType.FILE_NOT_FOUND] = 'Couldn\'t find the progr\
am {0}'
        self.errmessages[ErrorType.NO_RIGHTS] = 'Couldn\'t execute the program\
 {0}'
        self.errmessages[ErrorType.TIMEOUT] = 'Execution exceeded the {0}s tim\
eout'
        self.errmessages[ErrorType.SIGNALED] = 'Killed by signal {0}'
        self.errmessages[ErrorType.STDOUT_DIFFERS] = 'Standard output differs\
\nExpected:\n{0}\nGot:\n{1}'
        self.errmessages[ErrorType.STDERR_DIFFERS] = 'Standard error differs\n\
Expected:\n{0}\nGot:\n{1}'
        self.errmessages[ErrorType.RETURN_CODE_DIFFERS] = 'Return code differs\
\nExpected:\n{0}\nGot:\n{1}'
        self.chrome_messages = {}
        self.chrome_messages[Chrome.RAN_TESTS] = 'Ran {0} tests in {1:.1f} sec\
onds.\n'
        self.chrome_messages[Chrome.TESTS_STATS] = '[{0:.0f}%] Success: {1} | \
Errors: {3} | Failures: {2}\n'
        self.chrome_messages[Chrome.RAN_TEST] = '[{0}]{1}: {2}\n'

    def get_status_str(self, status):
        return self.status_messages[status]

    def get_error_str(self, error_type):
        return self.errmessages[error_type]

    def get_chrome_str(self, chrome_type):
        return self.chrome_messages[chrome_type]
