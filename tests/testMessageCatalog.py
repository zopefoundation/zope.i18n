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
"""

$Id: testMessageCatalog.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""
import unittest, sys

from Zope.I18n.MessageCatalog import MessageCatalog


class MessageCatalogTest(unittest.TestCase):

    def testConstructorAndOtherGetMethods(self):
        self.assertRaises(TypeError, MessageCatalog)
        
        msg_catalog = MessageCatalog('en')
        self.assertEqual(msg_catalog.getLanguage(), 'en')
        self.assertEqual(msg_catalog.getDomain(), 'global')
        self.assertEqual(msg_catalog.getIdentifier(), ('en', 'global'))

        msg_catalog = MessageCatalog('de', 'calendar')
        self.assertEqual(msg_catalog.getLanguage(), 'de')
        self.assertEqual(msg_catalog.getDomain(), 'calendar')
        self.assertEqual(msg_catalog.getIdentifier(), ('de', 'calendar'))


    def testSetGetAndQueryMessage(self):
        msg_catalog = MessageCatalog('de')
        
        msg_catalog.setMessage('greeting', 'Hallo mein Schatz!')
        self.assertEqual(msg_catalog.getMessage('greeting'),
                         'Hallo mein Schatz!')
        self.assertEqual(msg_catalog.queryMessage('greeting'),
                         'Hallo mein Schatz!')
        
        self.assertRaises(KeyError, msg_catalog.getMessage, ('hello'))
        self.assertEqual(msg_catalog.queryMessage('hello'),
                         'hello')
        self.assertEqual(msg_catalog.queryMessage('hello', 'greeting'),
                         'greeting')


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(MessageCatalogTest)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
