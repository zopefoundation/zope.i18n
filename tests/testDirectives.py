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

$Id: testDirectives.py,v 1.4 2002/06/20 15:55:08 jim Exp $
"""
import unittest
import os
from cStringIO import StringIO

from Zope.Configuration.xmlconfig import xmlconfig, Context, XMLConfig
from Zope.Configuration.Exceptions import ConfigurationError

from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup

import Zope.I18n
from Zope.I18n.GlobalTranslationService import translationService 

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
        XMLConfig('meta.zcml', Zope.I18n)()

    def testRegisterTranslations(self):
        eq = self.assertEqual
        eq(translationService._catalogs, {})
        xmlconfig(StringIO(template % (
            '''
            <gts:registerTranslations directory="./locale" />
            '''
            )), None, Context([], Zope.I18n.tests)) 
        path = os.path.join(Context([], Zope.I18n.tests).path(),
                            'locale', 'en',
                            'LC_MESSAGES', 'Zope-I18n.mo')
        eq(translationService._catalogs,
           {('en', 'Zope-I18n'): [unicode(path)]})

    def testDefaultLanguages(self):
        eq = self.assertEqual
        eq(translationService._fallbacks, ['en'])
        xmlconfig(StringIO(template % (
            '''
            <gts:defaultLanguages languages="de nl xx" />
            '''
            )), None, Context([], Zope.I18n.tests))
        eq(translationService._fallbacks, ['de', 'nl', 'xx'])


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(DirectivesTest)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())

