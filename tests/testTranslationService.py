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
import unittest, sys
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.I18n.IUserPreferedLanguages import IUserPreferedLanguages
from Zope.I18n.TranslationService import TranslationService
from Zope.I18n.MessageCatalog import MessageCatalog 
from types import StringType


class Environment:

    __implements__ = IUserPreferedLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getLanguages(self):
        return self.langs


class TestTranslationService(PlacelessSetup, unittest.TestCase):


    def testInterpolation(self):

        service = TranslationService()
        mapping = {'name': 'Zope', 'version': '3x'}

        self.assertEqual(service.interpolate('This is $name.', mapping),
                         'This is Zope.')
        self.assertEqual(service.interpolate('This is ${name}.', mapping),
                         'This is Zope.')

        self.assertEqual(service.interpolate(
            'This is $name version $version.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is ${name} version $version.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is $name version ${version}.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is ${name} version ${version}.', mapping),
                         'This is Zope version 3x.')
        

    def setUp(self):
        ''' '''
        PlacelessSetup.setUp(self)
        self._service = TranslationService('default') 

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')

        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')

        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')

        self._service.setObject('en-default-1', en_catalog)
        self._service.setObject('de-default-1', de_catalog)


    def testSimpleNoTranslate(self):
        service = self._service
        self.assertRaises(TypeError, service.translate, 'Hello')
    
        self.assertEqual(service.translate('default', 'short_greeting',
                                           target_language='es'),
                         'short_greeting')

        context = Environment()
        self.assertEqual(service.translate('default', 'short_greeting',
                                           context=context),
                         'short_greeting')
    
        self.assertRaises(TypeError, service.translate, 'short_greeting',
                          context=None)
    
    
    def testSimpleTranslate(self):
        ''' '''
        service = self._service
        self.assertEqual(service.translate('default', 'short_greeting',
                                           target_language='de'),
                         'Hallo!')

    
    def testDynamicTranslate(self):
        ''' '''
        service = self._service
    
        self.assertEqual(service.translate('default', 'greeting',
                                           mapping={'name': 'Stephan'},
                                           target_language='de'),
                         'Hallo Stephan, wie geht es Dir?')
        


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(TestTranslationService)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
