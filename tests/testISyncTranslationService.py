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
"""This is an 'abstract' test for the Synchronization Support interface.

$Id: testISyncTranslationService.py,v 1.1 2002/06/16 18:25:14 srichter Exp $
"""

import unittest
from Interface.Verify import verifyObject
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.I18n.ITranslationService import ISyncTranslationService


class TestISyncTranslationService(PlacelessSetup, unittest.TestCase):


    foreign_messages = [
        # Message that is not locally available
        {'domain': 'default', 'language': 'en', 'msgid': 'test',
         'msgstr': 'Test', 'mod_time': 0}, 
        # This message is newer than the local one.
        {'domain': 'default', 'language': 'de', 'msgid': 'short_greeting',
         'msgstr': 'Hallo.', 'mod_time': 20},
        # This message is older than the local one.
        {'domain': 'default', 'language': 'en', 'msgid': 'short_greeting',
         'msgstr': 'Hello', 'mod_time': 0},
        # This message is up-to-date.
        {'domain': 'default', 'language': 'en', 'msgid': 'greeting',
         'msgstr': 'Hello $name, how are you?', 'mod_time': 0}]


    local_messages = [
        # This message is older than the foreign one.
        {'domain': 'default', 'language': 'de', 'msgid': 'short_greeting',
         'msgstr': 'Hallo!', 'mod_time': 10},
        # This message is newer than the foreign one.
        {'domain': 'default', 'language': 'en', 'msgid': 'short_greeting',
         'msgstr': 'Hello!', 'mod_time': 10},
        # This message is up-to-date.
        {'domain': 'default', 'language': 'en', 'msgid': 'greeting',
         'msgstr': 'Hello $name, how are you?', 'mod_time': 0},
        # This message is only available locally. 
        {'domain': 'default', 'language': 'de', 'msgid': 'greeting',
         'msgstr': 'Hallo $name, wie geht es Dir?', 'mod_time': 0},
        ]
   

    # This should be overwritten by every clas that inherits this test
    def _getTranslationService(self):
        pass

    
    def setUp(self):
        PlacelessSetup.setUp(self)
        self._service = self._getTranslationService() 
        assert verifyObject(ISyncTranslationService, self._service)


    def testGetMessagesMapping(self):
        mapping = self._service.getMessagesMapping(['default'], ['de', 'en'],
                                                  self.foreign_messages)
        self.assertEqual(mapping[('test', 'default', 'en')],
                         (self.foreign_messages[0], None))
        self.assertEqual(mapping[('short_greeting', 'default', 'de')],
                         (self.foreign_messages[1], self.local_messages[0]))
        self.assertEqual(mapping[('short_greeting', 'default', 'en')],
                         (self.foreign_messages[2], self.local_messages[1]))
        self.assertEqual(mapping[('greeting', 'default', 'en')],
                         (self.foreign_messages[3], self.local_messages[2]))
        self.assertEqual(mapping[('greeting', 'default', 'de')],
                         (None, self.local_messages[3]))


    def testSynchronize(self):
        service = self._service
        mapping = service.getMessagesMapping(['default'], ['de', 'en'],
                                             self.foreign_messages)
        service.synchronize(mapping)

        self.assertEqual(service.getMessage('test', 'default', 'en'),
                         self.foreign_messages[0])
        self.assertEqual(service.getMessage('short_greeting', 'default', 'de'),
                         self.foreign_messages[1])
        self.assertEqual(service.getMessage('short_greeting', 'default', 'en'),
                         self.local_messages[1])
        self.assertEqual(service.getMessage('greeting', 'default', 'en'),
                         self.local_messages[2])
        self.assertEqual(service.getMessage('greeting', 'default', 'en'),
                         self.foreign_messages[3])
        self.assertEqual(service.getMessage('greeting', 'default', 'de'),
                         None)
        


        
def test_suite():
    pass
