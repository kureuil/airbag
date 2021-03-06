#!/usr/bin/env python3
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='airbag',
    version='0.5.0',
    description='Simple testrunner written in Python',
    author='Louis Person',
    author_email='lait.kureuil@gmail.com',
    url='https://github.com/kureuil/airbag',
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        airbag=airbag.application:cli
        [airbag.parsers]
        toml=airbag_toml.toml:TomlConfig [toml]
        [airbag.runners]
        prgm=airbag_program.runner:ProgramTest
        [airbag.formatters]
        cli=airbag_cli.cli:CliFormatter
    ''',
    extras_require={
        'toml': ['pytoml>=0.1.2']
    }
)
