# airbag

Simple testrunner written in Python.

# Installation

Clone this repo and run in a terminal `sudo python3 setup.py install`

# Usage

To use airbag, you need an airbag.toml in the current working directory. This file is used to define the tests that will run.

# Configuration

Configuration is done inside the `airbag.toml` file, written in [Toml](htpp://github.com/toml-lang/toml).

There's a table named `global` and a table array named `tests`. The `global` table properties' are scoped to all the tests. For each test you can define :

- `project` [string] : the project name
- `program` [string] : the default program to be run
- `name` [string] : the test's name
- `args` [array] : the default program arguments
- `expected` [string|table] : table to compare various things once a program executed. If it is a string, shortcut to compare stdout.
 - `output` [string] : expected standard output. Can be a file.
 - `errors` [string] : expected standard error. Can be a file.
 - `returncode` [integer] : expected exit code.

You can compare `expected.output` & `expected.errors` to a file contents by prefixing the file path with `file:`.

# Example

```toml

[global]
project = "Dummy project"
program = "foo"
args = []

[[tests]]
name = "It should work with invalid parameters"
args = ["Hello", "World", "--invalid-opt"]
expected = ""

[[tests]]
name = "Testing another program"
program = "echo"
args = ["-n", "Hello", "World"]
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
