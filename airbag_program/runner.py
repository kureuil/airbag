from subprocess import Popen, PIPE, DEVNULL, TimeoutExpired
from airbag.status import ExitStatus
from airbag.result import TestResult, ErrorType
from collections import ChainMap
from os import environ


class ProgramTest(object):
    """docstring for Test"""
    def __init__(
        self,
        program,
        name='',
        arguments=[],
        expected=None,
        stdin=None,
        timeout=15,
        emptyenv=False,
        env=None,
        reference=None
    ):
        super(ProgramTest, self).__init__()
        if program == '':
            raise ValueError('Missing program path')
        self.result = TestResult(name, program=program, arguments=arguments)
        self.program = program
        self.name = name
        self.arguments = arguments
        self.arguments.insert(0, self.program)
        self.expected = expected
        self.input = stdin
        self.timeout = timeout
        self.reference = reference
        if emptyenv is True:
            self.env = env if env is not None else None
        else:
            self.env = ChainMap(env, environ)

    def run(self):
        stdout = DEVNULL
        if 'output' in self.expected and len(self.expected['output']):
            stdout = PIPE
        stderr = DEVNULL
        if 'errors' in self.expected and len(self.expected['errors']):
            stderr = PIPE
        stdin = None
        if self.input is not None:
            stdin = PIPE
            if self.input.startswith('file:'):
                self.input = open(self.input[5:], 'rb').read()
            else:
                self.input = bytes(self.input, 'utf-8')
        try:
            p = Popen(
                self.arguments,
                env=self.env,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr
            )
        except FileNotFoundError:
            self.result.add_error(
                ErrorType.FILE_NOT_FOUND,
                program=self.program
            ).set_exit_status(ExitStatus.noexec)
            return self.result
        except PermissionError:
            self.result.add_error(ErrorType.NO_RIGHTS, self.program)
            self.result.set_exit_status(ExitStatus.noexec)
            return self.result

        try:
            outs, errs = p.communicate(self.input, self.timeout)
        except TimeoutExpired:
            p.kill()
            if 'timeout' not in self.expected:
                if self.expected['timeout'] is not True:
                    self.result.add_error(
                        ErrorType.TIMEOUT,
                        self.timeout
                    ).set_exit_status(ExitStatus.timeout)
                    return self.result
            return self.result

        if p.returncode < 0:
            self.result.add_error(ErrorType.SIGNALED, -p.returncode)
            self.result.set_exit_status(ExitStatus.killed)
            return self.result

        if 'output' in self.expected:
            if self.expected['output'].startswith('file:'):
                expected = open(self.expected['output'][5:], 'r').read()
            else:
                expected = self.expected['output']
            if outs is not None and outs.decode('utf-8') != expected:
                self.result.add_error(
                    ErrorType.STDOUT_DIFFERS,
                    expected,
                    outs.decode('utf-8')
                )

        if 'errors' in self.expected:
            if self.expected['errors'].startswith('file:'):
                expected = open(self.expected['errors'][5:], 'r').read()
            else:
                expected = self.expected['errors']
            if errs.decode('utf-8') != expected:
                self.result.add_error(
                    ErrorType.STDERR_DIFFERS,
                    expected,
                    errs.decode('utf-8')
                )

        if 'returncode' in self.expected:
            if self.expected['returncode'] != p.returncode:
                self.result.add_error(
                    ErrorType.RETURN_CODE_DIFFERS,
                    self.expected['returncode'],
                    p.returncode
                )

        if len(self.result.errors):
            self.result.set_exit_status(ExitStatus.finished)
        return self.result

    @staticmethod
    def get_type():
        return 'program'
