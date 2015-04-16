from subprocess import Popen, PIPE, TimeoutExpired

class Test(object):
	"""docstring for Test"""
	def __init__(self, program, name='', arguments=[], expected=''):
		super(Test, self).__init__()
		if program == '':
			raise ValueError('Missing program path')
		self.program = program
		self.name = name
		self.arguments = arguments
		self.expected = expected
		self.assertions = True

	def run(self):
		self.arguments.insert(0, self.program)
		p = Popen(self.arguments, stdout=PIPE, stderr=PIPE)
		try:
			outs, errs = p.communicate(timeout=15)
		except TimeoutExpired:
			p.kill()
			self.output('Timeout')
		else:
			if 'output' in self.expected.keys():
				if self.expected['output'].startswith('file:'):
					expected = open(self.expected['output'][5:], 'r').read()
				else:
					expected = self.expected['output']
				if outs.decode('utf-8') != expected:
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
			else:
				self.KO()
			return self.assertions
		return False

	def OK(self):
		self.output('OK')

	def KO(self):
		if self.assertions == True:
			self.assertions = False
			self.output('KO')

	def output(self, message):
		print('[{0}]{1}: {2}'.format(self.program, self.name, message))