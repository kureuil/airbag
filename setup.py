#!/usr/bin/env python3

from setuptools import setup

setup(name='airbag',
	  version='0.1.0',
	  description='Simple testrunner written in Python',
	  author='Louis Person',
	  author_email='lait.kureuil@gmail.com',
	  url='https://github.com/kureuil/airbag',
	  install_requires=['pytoml'],
	  packages=['airbag'],
	  entry_points='''
		[console_scripts]
		testrunner=airbag.application:cli
	  '''
	)