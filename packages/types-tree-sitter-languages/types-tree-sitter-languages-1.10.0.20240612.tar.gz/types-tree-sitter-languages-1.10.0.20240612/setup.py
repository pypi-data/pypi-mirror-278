from setuptools import setup

name = "types-tree-sitter-languages"
description = "Typing stubs for tree-sitter-languages"
long_description = '''
## Typing stubs for tree-sitter-languages

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`tree-sitter-languages`](https://github.com/grantjenks/py-tree-sitter-languages) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`tree-sitter-languages`.

This version of `types-tree-sitter-languages` aims to provide accurate annotations
for `tree-sitter-languages==1.10.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tree-sitter-languages. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `804a58165a59b88d933bc64b43172b3747ae9957` and was tested
with mypy 1.10.0, pyright 1.1.366, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.10.0.20240612",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tree-sitter-languages.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['tree-sitter>=0.20.3'],
      packages=['tree_sitter_languages-stubs'],
      package_data={'tree_sitter_languages-stubs': ['__init__.pyi', 'core.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
