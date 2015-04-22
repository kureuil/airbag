from sys import exit, version_info, stderr

if (version_info < (3, 3, 0)):
	stderr.write('Python 3.3 is required to run this program')
	exit(1)

from .testrunner import TestRunner
from .config.toml import TomlConfig

def cli():
	try:
		config = TomlConfig("airbag.toml")
	except ValueError:
		stderr.write('Error during configuration file parsing.\n')
		exit(1)
	except FileNotFoundError:
		exit(1)
	else:
		runner = TestRunner(config)
		if runner.launch() != 0:
			exit(1)