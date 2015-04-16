import sys
from .testrunner import TestRunner
from .config.toml import TomlConfig

def cli():
	try:
		config = TomlConfig("airbag.toml")
	except ValueError:
		print('Error during configuration file parsing. Aborting...')
		sys.exit(1)

	runner = TestRunner(config)
	if runner.launch() != 0:
		sys.exit(1)