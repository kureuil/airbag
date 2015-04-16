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
			get_key('program', raw, gconf, mandatory=True),
			get_key('name', raw, gconf, default=''),
			get_key('args', raw, gconf, default=[]),
			expected
		)
	except ValueError as e:
		print('An error occured: {0}', e.strerror)
		raise
	else:
		return test

def get_key(key, raw, gconf, mandatory=False, default=None):
	if key in raw.keys():
		return raw[key]
	elif key in gconf.keys():
		return gconf[key]
	else:
		if mandatory == False and default == None:
			return ''
		elif mandatory == False and default != None:
			return default
		else:
			raise ValueError('Missing required key {0}'.format(key))