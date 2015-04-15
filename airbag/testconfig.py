import pytoml
from .test import Test

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
		test = Test(
			get_key('program', raw, gconf),
			get_key('name', raw, gconf),
			get_key('args', raw, gconf),
			get_key('expected', raw, gconf)
		)
	except ValueError as e:
		print('An error occured: {0}', e.strerror)
		raise
	else:
		return test

def get_key(key, raw, gconf):
	if key in raw.keys():
		return raw[key]
	elif key in gconf.keys():
		return gconf[key]
	else:
		return ''

class TestConfig(object):
	"""docstring for TestConfig"""	
	def from_toml(filepath):
		with open(filepath, 'r') as rawfile:
			raw = pytoml.load(rawfile)
			gconf = parse_global(raw)
			tests = []
			for rtest in raw['tests']:
				try:
					test = parse_test(rtest, gconf)
				except ValueError:
					return {}
				else:
					tests.append(test)
			return tests
		return {}