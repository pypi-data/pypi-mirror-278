from setuptools import setup

name = "types-shapely"
description = "Typing stubs for shapely"
long_description = '''
## Typing stubs for shapely

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`shapely`](https://github.com/shapely/shapely) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`shapely`.

This version of `types-shapely` aims to provide accurate annotations
for `shapely==2.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/shapely. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `587ad6bad806a7c2fbc2bb5451007a9782bd665b` and was tested
with mypy 1.10.0, pyright 1.1.366, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.0.0.20240613",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/shapely.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['numpy>=1.20'],
      packages=['shapely-stubs'],
      package_data={'shapely-stubs': ['__init__.pyi', '_enum.pyi', '_geometry.pyi', '_ragged_array.pyi', '_typing.pyi', '_version.pyi', 'affinity.pyi', 'algorithms/__init__.pyi', 'algorithms/cga.pyi', 'algorithms/polylabel.pyi', 'constructive.pyi', 'coordinates.pyi', 'coords.pyi', 'creation.pyi', 'decorators.pyi', 'errors.pyi', 'geometry/__init__.pyi', 'geometry/base.pyi', 'geometry/collection.pyi', 'geometry/geo.pyi', 'geometry/linestring.pyi', 'geometry/multilinestring.pyi', 'geometry/multipoint.pyi', 'geometry/multipolygon.pyi', 'geometry/point.pyi', 'geometry/polygon.pyi', 'geos.pyi', 'io.pyi', 'lib.pyi', 'linear.pyi', 'measurement.pyi', 'ops.pyi', 'plotting.pyi', 'predicates.pyi', 'prepared.pyi', 'set_operations.pyi', 'speedups.pyi', 'strtree.pyi', 'testing.pyi', 'validation.pyi', 'vectorized/__init__.pyi', 'wkb.pyi', 'wkt.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
