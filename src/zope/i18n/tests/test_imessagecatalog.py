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
"""This is an 'abstract' test for the IMessageCatalog interface.

$Id$
"""
import unittest
from zope.interface.verify import verifyObject
from zope.i18n.interfaces import IMessageCatalog


class TestIMessageCatalog(unittest.TestCase):


    # This should be overwritten by every class that inherits this test
    def _getMessageCatalog(self):
        pass

    def _getUniqueIndentifier(self):
        pass


    def setUp(self):
        self._catalog = self._getMessageCatalog()

    def testInterface(self):
        verifyObject(IMessageCatalog, self._catalog)

    def testGetMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.getMessage('short_greeting'), 'Hello!')
        self.assertRaises(KeyError, catalog.getMessage, 'foo')


    def testQueryMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.queryMessage('short_greeting'), 'Hello!')
        self.assertEqual(catalog.queryMessage('foo'), None)
        self.assertEqual(catalog.queryMessage('foo', 'bar'), 'bar')

    def testGetPluralMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         'There is one file.')
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         'There are 3 files.')
        self.assertRaises(KeyError, catalog.getPluralMessage, 
                          'There are %d files.', 'bar', 6)

    def testQeuryPluralMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.queryPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         'There is one file.')
        self.assertEqual(catalog.queryPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         'There are 3 files.')
        self.assertEqual(catalog.queryPluralMessage(
                         'There are %d files.', 'There is one file.', 1,
                         'There is one file.', 'There are %d files.', ),
                         'There is one file.')
        self.assertEqual(catalog.queryPluralMessage(
                         'There are %d files.', 'There is one file.', 3,
                         'There is one file.', 'There are %d files.', ),
                         'There are 3 files.')
        
    def testGetLanguage(self):
        catalog = self._catalog
        self.assertEqual(catalog.language, 'en')


    def testGetDomain(self):
        catalog = self._catalog
        self.assertEqual(catalog.domain, 'default')


    def testGetIdentifier(self):
        catalog = self._catalog
        self.assertEqual(catalog.getIdentifier(), self._getUniqueIndentifier())


def test_suite():
    return unittest.TestSuite() # Deliberatly empty
