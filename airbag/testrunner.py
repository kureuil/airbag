from time import time

class TestRunner(object):
	"""docstring for TestRunner"""
	def __init__(self, config):
		super(TestRunner, self).__init__()
		self.tests = config.tests
	
	def launch(self):
		starttime = time()
		failures = 0
		for test in self.tests:
			if test.run() == False:
				failures += 1
		tests = len(self.tests)
		success = len(self.tests) - failures
		percentage = 0
		if tests > 0:
			percentage = success / tests * 100
		print('Ran {0} tests in {1:.1f} seconds.'.format(tests, time() - starttime))
		print('[{0:.0f}%] Success: {1} Failures: {2}'.format(percentage, success, failures))
		return failures