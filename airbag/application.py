from sys import exit, version_info, stderr

if (version_info < (3, 3, 0)):
	stderr.write('Python 3.3 is required to run this program')
	exit(1)

import argparse
from os import getcwd, chdir
from .testrunner import TestRunner
from .config.toml import TomlConfig

def cli():
	parser = argparse.ArgumentParser(
		description='Runs functional tests on your programs'
	)
	parser.add_argument(
		'-d', '--working-dir',
		type=str,
		metavar='DIR',
		default=getcwd(),
		help='Changes the working directory'
	)
	parser.add_argument(
		'-f', '--input-file',
		type=str,
		metavar='FILE',
		default='airbag.toml',
		help='Changes the configuration used'
	)
	parser.add_argument(
		'-V', '--version',
		action='version',
		version='Airbag 0.2',
		help='Displays the current program\'s version and exit'
	)
	args = parser.parse_args()
	try:
		config = TomlConfig(args.input_file)
	except ValueError:
		stderr.write('Error during configuration file parsing.\n')
		exit(1)
	except FileNotFoundError:
		exit(1)
	else:
		chdir(args.working_dir)
		runner = TestRunner(config)
		if runner.launch() != 0:
			exit(1)