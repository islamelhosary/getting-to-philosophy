# Contributing to Getting-to-Philosophy
:+1::tada: First of all, thanks for taking time to contribute to Getting-to-Philosophy  :tada::+1:

The following is a set of guidelines for contributing to Getting-to-Philosophy. Feel free to propose changes to this document in a pull request.

## What should I do before getting started?
### Get familiar with the code base
Before you get started, please take your time reading through the current code to get to know more about the coding style and structure.

### Pick your editor
A good editor can save you a lot of headache. Auto indentation, error hinting, auto complete, ...etc.

While there's no restriction on which editor you use, there are some suggestions to help you get started:

* [atom](https://atom.io/)
    * +plug-ins
        * [linter-python](https://atom.io/packages/linter-python) (pep8 and pyflakes)
        * [linter-pydocstyle](https://atom.io/packages/linter-pydocstyle) (for docstrings)
        * [autocomplete-python](https://atom.io/packages/autocomplete-python) (auto completion for python)
        * [python-indent](https://atom.io/packages/python-indent) (fixes atom python new line indentation)

### Install development requirements
```sh
# Make sure you're installing it outside your virtualenv
$ sudo pip install -r requirements-dev.txt
```
This installs necessary linting tools to check your code before sending a pull request.

## Styleguides
### Python Styleguides
All Python (with some few exceptions) must adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) and [PEP257](https://www.python.org/dev/peps/pep-0257/) ([Example Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)), also it should pass [pyflake](https://pypi.python.org/pypi/pyflakes). All of this is conveniently combined using [flake8](https://pypi.python.org/pypi/flake8) and is already configured for this project.

Running all these linters is as simple as:
```sh
$ flake8
```

## Sending a Pull Request
Before sending a pull request, make sure of the following:
* Code builds and runs correctly.
* Code passes all `flake8` tests.
