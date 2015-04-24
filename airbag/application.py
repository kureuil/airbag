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
    args = parser.parse_args()

    parsers = dict()
    for v in pkg_resources.iter_entry_points(group='airbag.parsers'):
        v = v.load()
        if v.get_extension() in parsers.keys():
            writerr(
                '{0}: duplicate parsers for this file type'.format(
                    v.get_extension()
                )
            )
        else:
            parsers[v.get_extension()] = v
    if len(parsers) is 0:
        writerr('no config parsers available. Aborting...')
        exit(1)

    runners = dict()
    for v in pkg_resources.iter_entry_points(group='airbag.runners'):
        v = v.load()
        if v.get_type() in runners.keys():
            writerr(
                '{0}: duplicate runners for this test type'.format(
                    v.get_type()
                )
            )
        else:
            runners[v.get_type()] = v
    if len(runners) is 0:
        writerr('no test runners available. Aborting...')
        exit(1)

    try:
        filename, fileext = path.splitext(args.input_file.name)
        config = parsers[fileext[1:]](args.input_file)
    except ValueError:
        writerr('{0}: error during parsing'.format(args.input_file.name))
        exit(1)

    if args.working_dir is not None:
        if path.exists(args.working_dir):
            chdir(args.working_dir)
        else:
            writerr(
                '{0}: directory does not exist'.format(args.working_dir)
            )
            exit(1)

    tests = []
    rtests = config.parse()
    for rtest in rtests:
        if 'type' in rtest.keys() and rtest['type'] is not None:
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
                    rtest['name'] if 'name' in rtest.keys() else '[unknown]'
                )
            )
    testrunner = TestRunner(tests)
    if testrunner.launch() != 0:
        exit(1)
