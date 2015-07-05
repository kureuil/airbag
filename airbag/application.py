try:
    from sys import exit, version_info, stderr
    import argparse
    import pkg_resources
    from os import getcwd, chdir, path
    from .error import write as writerr
    from .testrunner import TestRunner
except:
    if (version_info < (3, 3, 0)):
        stderr.write('Python 3.3+ is required to run this program')
        exit(1)


def cli_parse_args():
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
        type=argparse.FileType('r'),
        metavar='FILE',
        default='airbag.toml',
        help='Changes the configuration used'
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='Airbag 0.3',
        help='Displays the current program\'s version and exit'
    )
    return parser.parse_args() 


def get_parsers():
    parsers = dict()
    for v in pkg_resources.iter_entry_points(group='airbag.parsers'):
        v = v.load()
        if v.get_extension() in parsers:
            writerr(
                '{0}: duplicate parsers for this file type'.format(
                    v.get_extension()
                )
            )
        else:
            parsers[v.get_extension()] = v
    if not parsers:
        writerr('no config parsers available. Aborting...')
        exit(1)
    return parsers


def get_runners():
    runners = dict()
    for v in pkg_resources.iter_entry_points(group='airbag.runners'):
        v = v.load()
        if v.get_type() in runners:
            writerr(
                '{0}: duplicate runners for this test type'.format(
                    v.get_type()
                )
            )
        else:
            runners[v.get_type()] = v
    if not runners:
        writerr('no test runners available. Aborting...')
        exit(1) 
    return runners


def get_config(input_file, parsers):
    try:
        filename, fileext = path.splitext(input_file.name)
        config = parsers[fileext[1:]](input_file)
    except ValueError:
        writerr('{0}: error during parsing'.format(input_file.name))
        exit(1)
    return config


def change_working_dir(directory=None):
    if directory is not None:
        if path.exists(directory):
            chdir(directory)
        else:
            writerr(
                '{0}: directory does not exist'.format(directory)
            )
            exit(1)


def get_tests(config, runners):
    tests = []
    rtests = config.parse()
    for rtest in rtests:
        if 'type' in rtest and rtest['type'] is not None:
            try:
                runner = runners[rtest['type']]
                del rtest['type']
            except KeyError:
                writerr(
                    '{0}: no runner defined for this test type'.format(
                        rtest['type']
                    )
                )
                exit(1)
            tests.append(runner(**rtest))
        else:
            writerr(
                'no type defined for test \'{0}\''.format(
                    rtest['name'] if 'name' in rtest else '[unknown]'
                )
            )
    return tests


def cli():
    args = cli_parse_args()
    parsers = get_parsers()
    runners = get_runners()
    config = get_config(args.input_file, parsers)
    change_working_dir(args.working_dir)
    tests = get_tests(config, runners)
    testrunner = TestRunner(tests)
    if testrunner.launch() != 0:
        exit(1)
