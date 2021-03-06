# Airbag [![Build Status](https://travis-ci.org/kureuil/airbag.svg)](https://travis-ci.org/kureuil/airbag) [![Coverage Status](https://coveralls.io/repos/kureuil/airbag/badge.svg?branch=master&service=github)](https://coveralls.io/github/kureuil/airbag?branch=master)

Simple testrunner written in Python.

# Installation

Clone this repo and run in a terminal:

```bash
$ sudo python3 setup.py install
```

# Usage

```bash
$ airbag -h
usage: airbag [-h] [-d DIR] [-f FILE] [-V]

Runs functional tests on your programs

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --working-dir DIR
                        Changes the working directory
  -f FILE, --input-file FILE
                        Changes the configuration used
  -F FORMATTER, --formatter FORMATTER
                        Formatter used to display the output. Default is `cli`
  -O [OUTPUTS [OUTPUTS ...]], --out-fmt [OUTPUTS [OUTPUTS ...]]
                        Additional formatters to use with their file
                        destination
  -V, --version         Displays the current program\'s version and exit
```

By default, DIR will be the current working directory and FILE will be `airbag.toml`.

# Configuration

Configuration is done inside the `airbag.toml` file, written in [Toml](http://github.com/toml-lang/toml).

There's a table named `global` and a table array named `tests`. The `global` table properties' are scoped to all the tests. For each test you can define :

- `type` [string]\(**mandatory**): the test runner type
- `project` [string]\(default: `''`): the project name
- `program` [string]\(**mandatory**): the default program to be run
- `name` [string]\(default: `''`): the test's name
- `args` [array]\(default: `[]`): the default program arguments
- `input` [string]\(default: `''`): the program standard input
- `timeout` [int]\(default: `15`): time given to the program to finish its execution
- `emptyenv` [bool]\(default: `false`): should the environment be emptied before executing the program
- `env` [table]\(default: `{}`): environment keys to be set. Overrides already defined keys.
- `expected` [string|table]\(default: `''`): table to compare various things once a program executed. If it is a string, shortcut to compare stdout.
 - `output` [string]\(default: `''`): expected standard output. Can be a file.
 - `errors` [string]\(default: `''`): expected standard error. Can be a file.
 - `returncode` [integer]\(default: `0`): expected exit code.
 - `timeout` [bool]\(default: `false`): should the program timeout?

`input`, `expected.output` & `expected.errors` can be assigned a file contents by setting their value to the file path prefixed by `file:`.

## Configuration parsers

Configuration parsers in airbag are totally configurable. Anyone can write their own configuration parsers.

To register a configuration parser, register a class on the `airbag.parsers` entry point. TODO: document this feature, meanwhile see [toml.py](https://github.com/kureuil/airbag/blob/master/airbag_toml/toml.py).

For practical reasons, airbag ships with a toml configuration parsers.

## Test runners

As for configuration parsers, test runners are totally configurable.

To register a test runner, register a class on the `airbag.runners` entry point. TODO: document this feature, meanwhile see [runner.py](https://github.com/kureuil/airbag/blob/master/airbag_program/runner.py).

For practical reasons, airbag ships with a program test runner, which you can see an example below.

# Example

```toml

[global]
project = "Dummy project"
program = "foo"
args = []
type = "program"

[[tests]]
name = "It should work with invalid parameters"
args = ["Hello", "World", "--invalid-opt"]
expected = ""
emptyenv = true
    [tests.env]
    PATH = "/usr/bin"
    USER = "kureuil"

[[tests]]
name = "Testing another program"
program = "echo"
args = ["-n", "Hello", "World"]
timeout = 2
input = "file:input.txt"
    [tests.expected]
    returncode = 0
    errors = "file:empty-file.txt"
    output = "Hello World"

```

# License

The MIT License (MIT)

Copyright (c) 2015 Louis "Kureuil" Person

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
