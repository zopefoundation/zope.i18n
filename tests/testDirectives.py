##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
# 
##############################################################################
"""Test the gts ZCML namespace directives.

$Id: testDirectives.py,v 1.1 2002/06/12 18:38:58 srichter Exp $
"""
import unittest
import sys
import os
from cStringIO import StringIO

from Zope.Configuration.xmlconfig import xmlconfig, Context
from Zope.Configuration.Exceptions import ConfigurationError
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup


import Zope.I18n
defs_path = os.path.join(os.path.split(Zope.I18n.__file__)[0],
                         'i18n-meta.zcml')

template = """<zopeConfigure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:gts='http://namespaces.zope.org/gts'>
   xmlns:test='http://www.zope.org/NS/Zope3/test'>
   %s
   </zopeConfigure>"""


class DirectivesTest(PlacelessSetup, unittest.TestCase):

    # XXX: tests for other directives needed

    def setUp(self):
        PlacelessSetup.setUp(self)
        xmlconfig(open(defs_path))


    def testRegisterTranslations(self):
        from Zope.I18n.GlobalTranslationService import translationService 
             
        self.assertEqual(translationService._catalogs, {})

        from Zope.I18n import tests
        xmlconfig(StringIO(template % (
            '''
            <gts:registerTranslations directory="./locale" />
            '''
            )), None, Context([], tests)) 

        path = os.path.join(Context([], tests).path(), 'locale', 'en',
                            'LC_MESSAGES', 'Zope-I18n.mo')
        self.assertEqual(translationService._catalogs,
                         {('en', 'Zope-I18n'): [unicode(path)]})


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(DirectivesTest)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())

