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
"""This is an 'abstract' test for the IMessageCatalog interface.

$Id: test_iwritemessagecatalog.py,v 1.3 2002/12/31 02:52:15 jim Exp $
"""

import unittest
from zope.interface.verify import verifyObject
from zope.i18n.interfaces import IWriteMessageCatalog


class TestIWriteMessageCatalog(unittest.TestCase):


    # This should be overwritten by every class that inherits this test
    def _getMessageCatalog(self):
        pass

    def _getUniqueIndentifier(self):
        pass


    def setUp(self):
        self._catalog = self._getMessageCatalog()
        assert verifyObject(IWriteMessageCatalog, self._catalog)


    def testGetFullMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.getFullMessage('short_greeting'),
                         {'domain': 'default',
                          'language': 'en',
                          'msgid': 'short_greeting',
                          'msgstr': 'Hello!',
                          'mod_time': 0})


    def testSetMessage(self):
        catalog = self._catalog
        catalog.setMessage('test', 'Test', 1)
        self.assertEqual(catalog.getFullMessage('test'),
                         {'domain': 'default',
                          'language': 'en',
                          'msgid': 'test',
                          'msgstr': 'Test',
                          'mod_time': 1})
        catalog.deleteMessage('test')


    def testDeleteMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.queryMessage('test'), None)
        catalog.setMessage('test', 'Test', 1)
        self.assertEqual(catalog.queryMessage('test'), 'Test')
        catalog.deleteMessage('test')
        self.assertEqual(catalog.queryMessage('test'), None)


    def testGetMessageIds(self):
        catalog = self._catalog
        ids = catalog.getMessageIds()
        ids.sort()
        self.assertEqual(ids, ['greeting', 'short_greeting'])


    def testGetMessages(self):
        catalog = self._catalog
        ids = catalog.getMessageIds()
        ids.sort()
        self.assertEqual(ids, ['greeting', 'short_greeting'])


def test_suite():
    return unittest.TestSuite() # Deliberatly empty
