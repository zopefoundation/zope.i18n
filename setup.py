##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.i18n package

$Id$
"""

import os

try:
    from setuptools import setup, Extension
except ImportError, e:
    from distutils.core import setup, Extension

setup(name='zope.i18n',
      version='3.3-dev',
      url='http://svn.zope.org/zope.i18n',
      license='ZPL 2.1',
      description='Zope3 Internationalization Support',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      
      packages=['zope', 'zope.i18n'],
      package_dir = {'': 'src'},

      namespace_packages=['zope',],
      tests_require = ['zope.testing'],
      install_requires=['pytz',
                        'zope.component',
                        'zope.deprecation',
                        'zope.interface',
                        'zope.schema',
                       ],
      include_package_data = True,

      zip_safe = False,
      )
