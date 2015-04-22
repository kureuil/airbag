from subprocess import Popen, PIPE, DEVNULL, TimeoutExpired
from .status import ExitStatus

class Test(object):
	"""docstring for Test"""
	def __init__(self, program, name='', arguments=[], expected='', stdin=None, timeout=15):
		super(Test, self).__init__()
		if program == '':
			raise ValueError('Missing program path')
		self.program = program
		self.name = name
		self.arguments = arguments
		self.expected = expected
		self.assertions = True
		self.input = stdin
		self.timeout = timeout

	def run(self):
		self.arguments.insert(0, self.program)
		stdout = DEVNULL
		if 'output' in self.expected.keys() and len(self.expected['output']) != 0:
			stdout = PIPE
		stderr = DEVNULL
		if 'errors' in self.expected.keys() and len(self.expected['errors']) != 0:
			stderr = PIPE
		stdin = None
		if self.input != None:
			stdin = PIPE
			if self.input.startswith('file:'):
				self.input = open(self.input[5:], 'rb').read()
			else:
				self.input = bytes(self.input, 'utf-8')
		try:
			p = Popen(self.arguments, stdin=stdin, stdout=stdout, stderr=stderr)
		except FileNotFoundError:
			self.output('Couldn\'t find program {0}'.format(self.program))
			return ExitStatus.noexec
		except PermissionError:
			self.output('Couldn\'t execute program {0}'.format(self.program))
			return ExitStatus.noexec
		else:
			try:
				outs, errs = p.communicate(self.input, timeout=self.timeout)
			except TimeoutExpired:
				p.kill()
				self.output('Exceeding {0}s timeout'.format(self.timeout))
				return ExitStatus.timeout
			else:
				if p.returncode < 0:
					return ExitStatus.killed

				if 'output' in self.expected.keys():
					if self.expected['output'].startswith('file:'):
						expected = open(self.expected['output'][5:], 'r').read()
					else:
						expected = self.expected['output']
					if outs is not None and outs.decode('utf-8') != expected:
						self.KO()
						print('\tStandard output differ')
						print('\tExpected:\n{0}'.format(expected))
						print('\tOutput:\n{0}'.format(outs.decode("utf-8")))

				if 'errors' in self.expected.keys():
					if self.expected['errors'].startswith('file:'):
						expected = open(self.expected['errors'][5:], 'r').read()
					else:
						expected = self.expected['errors']
					if errs.decode('utf-8') != expected:
						self.KO()
						print('\tStandard error differ')
						print('\tExpected:\n{0}'.format(expected))
						print('\tOutput:\n{0}'.format(errs.decode('utf-8')))

				if 'returncode' in self.expected.keys():
					if self.expected['returncode'] != p.returncode:
						self.KO()
						print('\tReturn codes differ')
						print('\tExpected: {0}'.format(self.expected['returncode']))
						print('\tReturned: {0}'.format(p.returncode))

				if self.assertions == True:
					self.OK()
					return ExitStatus.ok
				else:
					self.KO()
					return ExitStatus.finished

	def OK(self):
		self.output('OK')

	def KO(self):
		if self.assertions == True:
			self.assertions = False
			self.output('KO')

	def output(self, message):
		print('[{0}]{1}: {2}'.format(self.program, self.name, message))