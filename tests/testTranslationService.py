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
from Zope.I18n.IUserPreferredLanguages import IUserPreferredLanguages
from Zope.I18n.TranslationService import TranslationService
from Zope.I18n.MessageCatalog import MessageCatalog 
from types import StringType


class Environment:

    __implements__ = IUserPreferredLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getPreferredLanguages(self):
        return self.langs


class TestTranslationService(PlacelessSetup, unittest.TestCase):

    def testInterpolation(self):
        service = TranslationService()
        mapping = {'name': 'Zope', 'version': '3x'}
        interp = service.interpolate
        eq = self.assertEqual
        # Test simple interpolations
        eq(interp('This is $name.', mapping), 'This is Zope.')
        eq(interp('This is ${name}.', mapping), 'This is Zope.')
        # Test more than one interpolation variable
        eq(interp('This is $name version $version.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is ${name} version $version.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is $name version ${version}.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is ${name} version ${version}.', mapping),
           'This is Zope version 3x.')
        # Test escaping the $
        eq(interp('This is $$name.', mapping), 'This is $$name.')
        eq(interp('This is $${name}.', mapping), 'This is $${name}.')

    def setUp(self):
        PlacelessSetup.setUp(self)
        self._service = TranslationService('default') 
        # Create an English and a German message catalog
        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')
        # Populate the catalogs with translations of a message id
        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')
        # And another message id with interpolation placeholders
        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')
        # Add the message catalogs to the translation service
        self._service.setObject('en-default-1', en_catalog)
        self._service.setObject('de-default-1', de_catalog)

    def testSimpleNoTranslate(self):
        service = self._service
        translate = service.translate
        raises = self.assertRaises
        eq = self.assertEqual
        # Test that we have at least the minimum required arguments
        raises(TypeError, translate, 'Hello')
        # Test that a translation in an unsupported language returns the
        # original message id unchanged.
        eq(translate('default', 'short_greeting', target_language='es'),
           'short_greeting')
        # Same test, but use the context argument instead of target_language
        context = Environment()
        eq(translate('default', 'short_greeting', context=context),
           'short_greeting')
        # Test that at least one of context or target_language is given
        raises(TypeError, translate, 'short_greeting', context=None)
    
    def testSimpleTranslate(self):
        service = self._service
        translate = service.translate
        eq = self.assertEqual
        # Test that a given message id is properly translated in a supported
        # language
        eq(translate('default', 'short_greeting', target_language='de'),
           'Hallo!')
        # Same test, but use the context argument
        context = Environment(('de', 'en'))
        eq(translate('default', 'short_greeting', target_language='de'),
           'Hallo!')

    def testDynamicTranslate(self):
        service = self._service
        translate = service.translate
        eq = self.assertEqual
        # Testing both translation and interpolation
        eq(translate('default', 'greeting', mapping={'name': 'Stephan'},
                     target_language='de'),
           'Hallo Stephan, wie geht es Dir?')

    def testParameterNames(self):
        service = self._service
        translate = service.translate
        eq = self.assertEqual
        raises = self.assertRaises
        # Test that the second argument is called `msgid'
        eq(translate('default', msgid='short_greeting', target_language='en'),
           'Hello!')
        # This is what the argument used to be called
        raises(TypeError, translate, 'default', source='short_greeting',
               target_language='en')

def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(TestTranslationService)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
