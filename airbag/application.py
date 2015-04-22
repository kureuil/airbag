from sys import exit, version_info

if (version_info < (3, 3, 0)):
	print('Python 3.3 is required to run this program')
	exit(1)

from .testrunner import TestRunner
from .config.toml import TomlConfig

def cli():
	try:
		config = TomlConfig("airbag.toml")
	except ValueError:
		print('Error during configuration file parsing. Aborting...')
		exit(1)

	runner = TestRunner(config)
	if runner.launch() != 0:
		exit(1)