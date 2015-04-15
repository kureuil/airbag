import subprocess

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

	def run(self):
		self.arguments.insert(0, self.program)
		p = subprocess.Popen(self.arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		try:
			outs, errs = p.communicate(timeout=15)
		except TimeoutExpired:
			p.kill()
			self.output('Timeout')
		else:
			if self.expected.startswith('file:'):
				expected = open(self.expected[5:], 'r').read()
			else:
				expected = self.expected
			if outs.decode('utf-8') == expected:
				self.output('OK')
				return True
			self.output('KO')
			print('Expected: {0}'.format(expected))
			print('Output: {0}'.format(outs.decode("utf-8")))
		return False

	def output(self, message):
		print('[{0}]{1}: {2}'.format(self.program, self.name, message))