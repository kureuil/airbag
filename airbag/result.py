from enum import Enum
from airbag.status import ExitStatus


class TestResult(object):
    def __init__(self, name, program='', arguments=[]):
        super(TestResult, self).__init__()
        self.status = ExitStatus.OK
        self.errors = []
        self.name = name
        self.program = program
        self.arguments = arguments

    def set_exit_status(self, exit_status):
        self.status = exit_status
        return self

    def add_error(self, error_type, *args):
        self.errors.append(dict(type=error_type, args=args))
        return self


class ErrorType(Enum):
    FILE_NOT_FOUND = 1
    NO_RIGHTS = 2
    TIMEOUT = 3
    SIGNALED = 4
    STDOUT_DIFFERS = 5
    STDERR_DIFFERS = 6
    RETURN_CODE_DIFFERS = 7
