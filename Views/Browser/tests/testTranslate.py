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

$Id: testTranslate.py,v 1.1 2002/06/12 18:38:57 srichter Exp $
"""

import unittest
from cStringIO import StringIO

from Zope.I18n.Views.Browser.Translate import Translate
from Zope.I18n.TranslationService import TranslationService
from Zope.I18n.MessageCatalog import MessageCatalog

from Zope.Publisher.Browser.BrowserRequest import BrowserRequest


# Setup the registries
from Zope.ComponentArchitecture.IFactoryService import IFactoryService
from Zope.ComponentArchitecture.GlobalFactoryService import \
     factoryService
from Zope.App.ComponentArchitecture.metaConfigure import \
     provideService, managerHandler
from Zope.App.ComponentArchitecture.metaConfigure import handler

    
class TranslateTest(unittest.TestCase):

    def setUp(self):

        try:
            # Setup the registries
            managerHandler('defineService', 'Factories', IFactoryService) 
            provideService('Factories', factoryService, 'Zope.Public')
            
            handler('Factories', 'provideFactory', 'Message Catalog',
                    MessageCatalog)
        except:
            pass
        
        service = TranslationService('default') 

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')

        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')

        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')

        service.setObject('en-default-1', en_catalog)
        service.setObject('de-default-1', de_catalog)

        self._view = Translate(service, self._getRequest())
        

    def _getRequest(self, **kw):
        request = BrowserRequest(StringIO(''), StringIO(), kw)
        request._cookies = {'edit_domains': 'default',
                            'edit_languages': 'en,de'}
        request._traversed_names = ['foo', 'bar']
        return request


    def testGetMessages(self):
        ids = map(lambda m: m[0], self._view.getMessages())
        ids.sort()
        self.assertEqual(ids, ['greeting', 'short_greeting'])


    def testGetTranslation(self):
        self.assertEqual(self._view.getTranslation('default', 'short_greeting',
                                                   'en'),
                         'Hello!')


    def testGetAllLanguages(self):
        languages = self._view.getAllLanguages()
        languages.sort()
        self.assertEqual(languages, ['de', 'en'])


    def testGetAllDomains(self):
        domains = self._view.getAllDomains()
        domains.sort()
        self.assertEqual(domains, ['default'])

        
    def testGetEditLanguages(self):
        languages = self._view.getEditLanguages()
        languages.sort()
        self.assertEqual(languages, ['de', 'en'])


    def testGetEditDomains(self):
        domains = self._view.getEditDomains()
        domains.sort()
        self.assertEqual(domains, ['default'])


    # def testEditMessages(self):
    #     pass
    # 
    # def testDeleteMessages(self):
    #     pass
        
    def testAddDeleteLanguage(self):
        self._view.addLanguage('es')
        assert 'es' in self._view.getAllLanguages()
        self._view.deleteLanguages(['es'])
        assert 'es' not in self._view.getAllLanguages()


    def testAddDeleteDomain(self):
        self._view.addDomain('Zope')
        assert 'Zope' in self._view.getAllDomains()
        self._view.deleteDomains(['Zope'])
        assert 'Zope' not in self._view.getAllDomains()


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase( TranslateTest )

if __name__=='__main__':
    unittest.main()
