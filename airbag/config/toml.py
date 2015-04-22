import pytoml
from .base import BaseConfig
from ..test import Test

class TomlConfig(BaseConfig):
	"""docstring for TomlConfig"""
	def __init__(self, filepath):
		super(TomlConfig, self).__init__()
		self.filepath = filepath
		self.parse()
	
	def parse(self):
		with open(self.filepath, 'r') as rawfile:
			raw = pytoml.load(rawfile)
			gconf = parse_global(raw)
			for rtest in raw['tests']:
				try:
					test = parse_test(rtest, gconf)
				except ValueError:
					return {}
				else:
					self.tests.append(test)

def parse_global(raw):
	keys = ['program', 'project', 'args', 'expected']
	gconf = {}
	if 'global' not in raw.keys():
		return gconf
	for key in keys:
		if key in raw['global'].keys():
			gconf[key] = raw['global'][key]
	return gconf

def parse_test(raw, gconf):
	try:
		expected = get_key('expected', raw, gconf, default='')
		if type(expected) is str:
			expected = dict(output=expected)
		test = Test(
			program = get_key('program', raw, gconf, mandatory=True),
			name = get_key('name', raw, gconf, default=''),
			arguments = get_key('args', raw, gconf, default=[]),
			expected = expected,
			stdin = get_key('input', raw, gconf),
			timeout = get_key('timeout', raw, gconf, default=15)
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
		if mandatory == False:
			return default
		else:
			raise ValueError('Missing required key {0}'.format(key))