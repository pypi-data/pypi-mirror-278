from setuptools import setup

name = "types-jsonschema"
description = "Typing stubs for jsonschema"
long_description = '''
## Typing stubs for jsonschema

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`jsonschema`](https://github.com/python-jsonschema/jsonschema) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`jsonschema`.

This version of `types-jsonschema` aims to provide accurate annotations
for `jsonschema==4.22.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/jsonschema. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `0c45de1c2667ca52428f2fc0ec9ba07f5d7d4aee` and was tested
with mypy 1.10.0, pyright 1.1.366, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="4.22.0.20240610",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/jsonschema.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['referencing'],
      packages=['jsonschema-stubs'],
      package_data={'jsonschema-stubs': ['__init__.pyi', '_format.pyi', '_keywords.pyi', '_legacy_keywords.pyi', '_types.pyi', '_typing.pyi', '_utils.pyi', 'cli.pyi', 'exceptions.pyi', 'protocols.pyi', 'validators.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
