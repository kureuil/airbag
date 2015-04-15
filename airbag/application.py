import sys
from .testrunner import TestRunner
from .testconfig import TestConfig

def cli():
	config = TestConfig.from_toml("airbag.toml")
	if config == {}:
		sys.exit(1)
	runner = TestRunner(config)
	if runner.launch() != 0:
		sys.exit(1)