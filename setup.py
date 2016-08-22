#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
import platform
py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'
IS_JYTHON = py_impl() == 'Jython'


entry_points = {
    'console_scripts': [
        'plastex = plasTeX.plastex:main'
    ]
}

TESTS_REQUIRE = [
    'beautifulsoup4',
    'zope.testrunner',
    'pyhamcrest',
]

INSTALL_REQUIRES = [
    # Chameleon for template rendering.
    'Chameleon',
    'z3c.pt >= 3.0.0a1',  # Better ZPT support than plastex, add-in to Chameleon
    'z3c.ptcompat >= 2.0.0a1',  # Make zope.pagetemplate also use the Chameleon-based ZPT
    'zope.pagetemplate >= 4.0.4', # pulled in by z3c.ptcompat, pin to newer version

    # tal/tales for expression language in zpt templates
    'zope.tal >= 4.0.0a1',
    'zope.tales >= 4.0.1',

    'Pillow',

    'six', # py3/py2 compat

    'zope.annotation',
    'zope.cachedescriptors >= 4.0.0',
    'zope.component',
    'zope.configuration',
    'zope.dottedname',
    'zope.dublincore',
    'zope.event >= 4.0.2', # implicit dep of zope.component/interface
    'zope.exceptions',
    'zope.i18n >= 4.0.0a4', # implicit dep of Chameleon
    'zope.i18nmessageid >= 4.0.2',
    'zope.interface',
    'zope.location',
    'zope.proxy',  # 4.1.x support py3k, uses newer APIs. Not binary compat with older extensions, must rebuild. (In partic, req zope.security >= 3.9)
    'zope.traversing >= 4.0.0a3', # tal/tales paths, also our own traversing implementation
]

def read(name):
    with open(join(dirname(__file__), name)) as f:
        return f.read().strip()

def alltests():
    import os
    import sys
    import unittest
    # use the zope.testrunner machinery to find all the
    # test suites we've put under ourselves.
    # Based on zope.principalregistry
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    args = sys.argv[:]
    defaults = ["--test-path", here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)

setup(name="nti.plasTeX",
      description="Modern, extensible, LaTeX document processing framework",
      long_description=read('README.rst'),
      version="0.9.3",
      author="Kevin D. Smith",
      author_email="Kevin.Smith@sas.com",
      url="https://github.com/NextThought/nti.plasTeX",
      keywords='latex render zope tal zpt html DOM',
      license='Apache',
      tests_require=TESTS_REQUIRE,
      install_requires=INSTALL_REQUIRES,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Programming Language :: Python :: Implementation :: Jython",
          "Operating System :: MacOS :: MacOS X",
          "Framework :: Zope3",
      ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      entry_points=entry_points,
      extras_require={
          'test': TESTS_REQUIRE,
          'tools': [
              'repoze.sphinx.autointerface >= 0.7.1',
              'sphinx >= 1.2b1',  # Narrative docs
            ]
      },
      dependency_links=[
      ],
      #test_loader="zope.testrunner.eggsupport:SkipLayers",
      test_suite="__main__.alltests",
)
