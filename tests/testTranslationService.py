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
"""This module tests the regular persistent Translation Service.

$Id: testTranslationService.py,v 1.5 2002/06/13 13:13:08 srichter Exp $
"""
import unittest, sys

from Zope.I18n.TranslationService import TranslationService
from Zope.I18n.MessageCatalog import MessageCatalog 
from testITranslationService import TestITranslationService
from testIEditableTranslationService import TestIEditableTranslationService

class TestTranslationService(TestIEditableTranslationService,
                             TestITranslationService):

    def _getTranslationService(self):
        service = TranslationService('default') 

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')
        # Populate the catalogs with translations of a message id
        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')
        # And another message id with interpolation placeholders
        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')

        service.setObject('en-default-1', en_catalog)
        service.setObject('de-default-1', de_catalog)

        return service

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
