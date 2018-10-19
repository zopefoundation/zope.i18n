##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.i18n package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

def alltests():
    import sys
    import unittest
    # use the zope.testrunner machinery to find all the
    # test suites we've put under ourselves
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    args = sys.argv[:]
    defaults = ["--test-path", here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)

COMPILE_REQUIRES = [
    # python-gettext used to be here, but it's now
    # a fixed requirement. Keep the extra to avoid
    # breaking downstream installs.
]

ZCML_REQUIRES = [
    'zope.component[zcml]',
    'zope.configuration',
    'zope.security',
]

TESTS_REQUIRE = COMPILE_REQUIRES + ZCML_REQUIRES + [
    'zope.publisher',
    'zope.testing',
    'zope.testrunner',
]

setup(
    name='zope.i18n',
    version='4.5',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    description='Zope Internationalization Support',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    license='ZPL 2.1',
    keywords=('zope3 internationalization localization i18n l10n '
              'gettext ICU locale'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/zope.i18n',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope',],
    install_requires=[
        'setuptools',
        'python-gettext',
        'pytz',
        'zope.deprecation',
        'zope.schema',
        'zope.i18nmessageid >= 4.3',
        'zope.component',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'compile': COMPILE_REQUIRES,
        'zcml': ZCML_REQUIRES,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
        ],
    },
    tests_require=TESTS_REQUIRE,
    test_suite='__main__.alltests',
    include_package_data=True,
    zip_safe=False,
    )
