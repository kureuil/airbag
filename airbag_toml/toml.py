import pytoml


class TomlConfig(object):
    """docstring for TomlConfig"""
    def __init__(self, contents):
        super(TomlConfig, self).__init__()
        self.raw = pytoml.load(contents)

    def parse(self):
        tests = []
        gconf = {}
        if 'global' in self.raw.keys():
            for key, value in self.raw['global'].items():
                gconf[key] = value
        for rtest in self.raw['tests']:
            try:
                test = parse_test(rtest, gconf)
            except ValueError:
                raise
            tests.append(test)
        return tests

    def get_extension():
        return 'toml'


def parse_test(raw, gconf):
    try:
        expected = get_key('expected', raw, gconf, default='')
        if type(expected) is str:
            expected = dict(output=expected)
        test = dict(
            program=get_key('program', raw, gconf, mandatory=True),
            name=get_key('name', raw, gconf, default=''),
            arguments=get_key('args', raw, gconf, default=[]),
            expected=expected,
            stdin=get_key('input', raw, gconf),
            timeout=get_key('timeout', raw, gconf, default=15),
            emptyenv=get_key('emptyenv', raw, gconf, default=False),
            env=get_key('env', raw, gconf),
            reference=get_key('ref', raw, gconf),
            type=get_key('type', raw, gconf)
        )
    except ValueError as e:
        raise
    return test


def get_key(key, raw, gconf, mandatory=False, default=None):
    if key in raw.keys():
        return raw[key]
    elif key in gconf.keys():
        return gconf[key]
    else:
        if mandatory is False:
            return default
        else:
            raise ValueError('Missing required key {0}'.format(key))
