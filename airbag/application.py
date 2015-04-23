try:
    from sys import exit, version_info, stderr
    import argparse
    import pkg_resources
    from os import getcwd, chdir, path
    from .error import write as writerr
    from .testrunner import TestRunner
    from .test import Test
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
        version='Airbag 0.2',
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
    try:
        filename, fileext = path.splitext(args.input_file.name)
        config = parsers[fileext[1:]](args.input_file)
    except ValueError:
        writerr('{0}: error during parsing'.format(args.input_file.name))
        exit(1)
    else:
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
            tests.append(Test(**rtest))
        runner = TestRunner(tests)
        if runner.launch() != 0:
            exit(1)
