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
"""This is an 'abstract' test for the ITranslationService interface.

$Id: test_iwritetranslationservice.py,v 1.2 2002/12/25 14:13:40 jim Exp $
"""

import unittest

from zope.interface.verify import verifyObject
from zope.component.tests.placelesssetup import PlacelessSetup

# XXX Bad, can't depend on app!
from zope.app.component.metaconfigure import provideService, managerHandler

from zope.i18n.negotiator import negotiator
from zope.interfaces.i18n import INegotiator
from zope.interfaces.i18n import IUserPreferredLanguages
from zope.interfaces.i18n import ITranslationService
from zope.interfaces.i18n import IDomain

class Environment:

    __implements__ = IUserPreferredLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getPreferredLanguages(self):
        return self.langs



class TestIWriteTranslationService(PlacelessSetup, unittest.TestCase):

    def _getTranslationService(self):
        """This should be overwritten by every clas that inherits this test.

           We expect the TranslationService to contain exactly 2 languages:
           de and en
        """


    def setUp(self):
        PlacelessSetup.setUp(self)
        self._service = self._getTranslationService()
        assert verifyObject(ITranslationService, self._service)
        managerHandler('defineService', 'Translation',
                       ITranslationService)
        provideService('Translation', self._service, 'zope.Public')

        # Setup the negotiator service registry entry
        managerHandler('defineService', 'LanguageNegotiation', INegotiator)
        provideService('LanguageNegotiation', negotiator, 'zope.Public')


    def _getDomains(self, service):
        domains = service.getAllDomains()
        domains.sort()
        return domains


    def testGetAddDeleteDomain(self):
        service = self._service
        service.addLanguage('de')
        d = self._getDomains(service)
        self.assertEqual(service.getAllDomains(), d+[])
        service.addDomain('test')
        self.assertEqual(service.getAllDomains(), d+['test'])
        service.addDomain('test2')
        self.assertEqual(service.getAllDomains(), d+['test', 'test2'])
        self.assertEqual(service.getAvailableDomains('de'),
                         d+['test', 'test2'])
        service.deleteDomain('test')
        self.assertEqual(service.getAllDomains(), d+['test2'])
        service.deleteDomain('test2')
        self.assertEqual(service.getAllDomains(), d+[])


    def _getLanguages(self, service):
        languages = service.getAllLanguages()
        languages.sort()
        return languages


    def testGetAddDeleteLanguage(self):
        service = self._service
        service.addDomain('test')
        langs = self._getLanguages(service)
        service.addLanguage('es')
        self.assertEqual(self._getLanguages(service), langs+['es'])
        service.addLanguage('fr')
        self.assertEqual(self._getLanguages(service), langs+['es', 'fr'])
        self.assertEqual(service.getAvailableLanguages('test'),
                         langs+['es', 'fr'])
        service.deleteLanguage('es')
        self.assertEqual(self._getLanguages(service), langs+['fr'])
        service.deleteLanguage('fr')
        self.assertEqual(self._getLanguages(service), langs)


    def testAddUpdateDeleteMessage(self):
        service = self._service
        self.assertEqual(service.translate('test', 'greeting',
                                           target_language='de'), 'greeting')
        service.addMessage('test', 'greeting', 'Hallo!', 'de')
        self.assertEqual(service.translate('test', 'greeting',
                                           target_language='de'), 'Hallo!')
        service.updateMessage('test', 'greeting', 'Hallo Ihr da!', 'de')
        self.assertEqual(service.translate('test', 'greeting',
                                           target_language='de'),
                         'Hallo Ihr da!')
        service.deleteMessage('test', 'greeting', 'de')
        self.assertEqual(service.translate('test', 'greeting',
                                           target_language='de'), None)


    def _getMessageIds(self, service, domain, filter="%"):
        ids = service.getMessageIdsOfDomain(domain, filter)
        ids.sort()
        return ids


    def testFilteredGetAllMessageIdsOfDomain(self):
        service = self._service
        service.addMessage('test',  'greeting', 'Greeting!', 'en')
        service.addMessage('test',  'greeting2', 'Greeting 2!', 'en')
        service.addMessage('test2', 'greeting3', 'Greeting 3!', 'en')
        service.addMessage('test2', 'greeting4', 'Greeting 4!', 'en')

        self.assertEqual(self._getMessageIds(service, 'test'),
                         ['greeting', 'greeting2'])
        self.assertEqual(self._getMessageIds(service, 'test2'),
                         ['greeting3', 'greeting4'])
        self.assertEqual(self._getMessageIds(service, 'test', 'greeting'),
                         ['greeting', 'greeting2'])
        self.assertEqual(self._getMessageIds(service, 'test', '%2'),
                         ['greeting2'])
        self.assertEqual(self._getMessageIds(service, 'test', 'gre%2'),
                         ['greeting2'])
        self.assertEqual(self._getMessageIds(service, 'test2', 'gre%'),
                         ['greeting3', 'greeting4'])


def test_suite():
    return unittest.TestSuite() # Deliberatly empty
