from .status import ExitStatus
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
        self.errmessages[ErrorType.FILE_NOT_FOUND] = 'Couldn\'t find the progra\
m {0}'
        self.errmessages[ErrorType.NO_RIGHTS] = 'Couldn\'t execute the program \
{0}'
        self.errmessages[ErrorType.TIMEOUT] = 'Execution exceeded the {0}s time\
out'
        self.errmessages[ErrorType.SIGNALED] = 'Killed by signal {0}'
        self.errmessages[ErrorType.STDOUT_DIFFERS] = 'Standard output differs\n\
Expected:\n{0}\nGot:\n{1}\n'
        self.errmessages[ErrorType.STDERR_DIFFERS] = 'Standard error differs\n\
Expected:\n{0}\nGot:\n{1}\n'
        self.errmessages[ErrorType.RETURN_CODE_DIFFERS] = 'Return code differs\
\nExpected:\n{0}\nGot:\n{1}\n'

    def get_status_str(self, status):
        return self.status_messages[status]

    def get_error_str(self, error_type):
        return self.errmessages[error_type]
