# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cytriangle']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.25.2,<2.0.0']

setup_kwargs = {
    'name': 'cytriangle',
    'version': '1.0.0',
    'description': "Object-oriented Cython wrapper of Shewchuk's Triangle Library",
    'long_description': '# CyTriangle\n## A Python Wrapped Triangle Library via Cython\n\n![ci-tests](https://github.com/m-clare/cytriangle/actions/workflows/ci.yaml/badge.svg)\n![code style](https://img.shields.io/badge/code%20style-black-000000.svg)\n![license](https://img.shields.io/github/license/m-clare/cytriangle)\n\n*CyTriangle* is an object-oriented python wrapper around Jonathan Richard Shewchuk\'s [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) library. From its documentation:\n\n"Triangle generates exact Delaunay triangulations, constrained Delaunay triangulations, conforming Delaunay triangulations, Voronoi diagrams, and high-quality triangular meshes. The latter can be generated with no small or large angles, and are thus suitable for finite element analysis."\n\n*CyTriangle* utilizes Cython to provide an object-oriented interface to Triangle to enable easier inspection and modification of triangle objects.\n',
    'author': 'Maryanne Wachter',
    'author_email': 'mclare@utsv.net',
    'maintainer': 'Maryanne Wachter',
    'maintainer_email': 'mclare@utsv.net',
    'url': 'https://github.com/m-clare/cytriangle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
