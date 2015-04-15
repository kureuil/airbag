from time import time

class TestRunner(object):
	"""docstring for TestRunner"""
	def __init__(self, tests):
		super(TestRunner, self).__init__()
		self.tests = tests
	
	def launch(self):
		starttime = time()
		failures = 0
		for test in self.tests:
			if test.run() == False:
				failures += 1
		print('Ran {0} tests in {1:.1f} seconds.'.format(len(self.tests), time() - starttime))
		print('{0} of them failed.'.format(failures))
		return failures