##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Test the gts ZCML namespace directives.

$Id$
"""
import os
import unittest

import zope.component
import zope.i18n.tests
from zope.component.testing import PlacelessSetup
from zope.configuration import xmlconfig
from zope.i18n.interfaces import ITranslationDomain

template = """\
<configure
    xmlns='http://namespaces.zope.org/zope'
    xmlns:i18n='http://namespaces.zope.org/i18n'>
  %s
</configure>"""

class DirectivesTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(DirectivesTest, self).setUp()
        self.context = xmlconfig.file('meta.zcml', zope.i18n)

    def testRegisterTranslations(self):
        self.assert_(zope.component.queryUtility(ITranslationDomain) is None)
        xmlconfig.string(
            template % '''
            <configure package="zope.i18n.tests">
            <i18n:registerTranslations directory="locale" />
            </configure>
            ''', self.context)
        path = os.path.join(os.path.dirname(zope.i18n.tests.__file__),
                            'locale', 'en', 'LC_MESSAGES', 'zope-i18n.mo')
        util = zope.component.getUtility(ITranslationDomain, 'zope-i18n')
        self.assertEquals(util._catalogs,
                          {'test': ['test'], 'en': [unicode(path)]})

    def testRegisterDistributedTranslations(self):
        self.assert_(zope.component.queryUtility(ITranslationDomain) is None)
        xmlconfig.string(
            template % '''
            <configure package="zope.i18n.tests">
            <i18n:registerTranslations directory="locale" />
            </configure>
            ''', self.context)
        xmlconfig.string(
            template % '''
            <configure package="zope.i18n.tests">
            <i18n:registerTranslations directory="locale2" />
            </configure>
            ''', self.context)
        path1 = os.path.join(os.path.dirname(zope.i18n.tests.__file__),
                             'locale', 'en', 'LC_MESSAGES', 'zope-i18n.mo')
        path2 = os.path.join(os.path.dirname(zope.i18n.tests.__file__),
                             'locale2', 'en', 'LC_MESSAGES', 'zope-i18n.mo')
        util = zope.component.getUtility(ITranslationDomain, 'zope-i18n')
        self.assertEquals(util._catalogs,
                          {'test': ['test', 'test'],
                                   'en': [unicode(path1), unicode(path2)]})

        msg = util.translate(u'Additional message', target_language='en')
        self.assertEquals(msg, u'Additional message translated')

        msg = util.translate(u'New Domain', target_language='en')
        self.assertEquals(msg, u'New Domain translated')

        msg = util.translate(u'New Language', target_language='en')
        self.assertEquals(msg, u'New Language translated')


def test_suite():
    return unittest.makeSuite(DirectivesTest)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
