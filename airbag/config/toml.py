import pytoml
from sys import stderr
from .base import BaseConfig
from ..test import Test


class TomlConfig(BaseConfig):
    """docstring for TomlConfig"""
    def __init__(self, contents):
        super(TomlConfig, self).__init__()
        raw = pytoml.load(contents)
        gconf = parse_global(raw)
        self.tests = []
        for rtest in raw['tests']:
            try:
                test = parse_test(rtest, gconf)
            except ValueError:
                raise
            else:
                self.tests.append(test)


def parse_global(raw):
    gconf = {}
    if 'global' in raw.keys():
        for key, value in raw['global'].items():
            gconf[key] = value
    return gconf


def parse_test(raw, gconf):
    try:
        expected = get_key('expected', raw, gconf, default='')
        if type(expected) is str:
            expected = dict(output=expected)
        test = Test(
            program=get_key('program', raw, gconf, mandatory=True),
            name=get_key('name', raw, gconf, default=''),
            arguments=get_key('args', raw, gconf, default=[]),
            expected=expected,
            stdin=get_key('input', raw, gconf),
            timeout=get_key('timeout', raw, gconf, default=15),
            emptyenv=get_key('emptyenv', raw, gconf, default=False),
            env=get_key('env', raw, gconf),
            reference=get_key('ref', raw, gconf)
        )
    except ValueError as e:
        raise
    else:
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
