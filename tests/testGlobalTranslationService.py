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

$Id: testGlobalTranslationService.py,v 1.4 2002/06/18 18:24:30 bwarsaw Exp $
"""
import unittest, sys, os
from Zope.I18n.GlobalTranslationService import GlobalTranslationService
from Zope.I18n.GettextMessageCatalog import GettextMessageCatalog 
from testIReadTranslationService import TestIReadTranslationService, \
     Environment

def testdir():
    from Zope.I18n import tests
    return os.path.dirname(tests.__file__)


class TestGlobalTranslationService(TestIReadTranslationService):

    def _getTranslationService(self):
        service = GlobalTranslationService('default') 
        path = testdir()
        en_catalog = GettextMessageCatalog('en', 'default',
                                           os.path.join(path, 'en-default.mo'))
        de_catalog = GettextMessageCatalog('de', 'default',
                                           os.path.join(path, 'de-default.mo'))
        service.addCatalog(en_catalog)
        service.addCatalog(de_catalog)
        return service

    def testSimpleNoTranslate(self):
        translate = self._service.translate
        raises = self.assertRaises
        eq = self.assertEqual
        # Unset fallback translation languages
        self._service.setLanguageFallbacks([])
        # Test that we have at least the minimum required arguments
        raises(TypeError, translate, 'Hello')
        # Test that a translation in an unsupported language returns the
        # original message id unchanged, if there is no fallback language
        eq(translate('default', 'short_greeting', target_language='es'),
           'short_greeting')
        # Same test, but use the context argument instead of target_language
        context = Environment()
        eq(translate('default', 'short_greeting', context=context),
           'short_greeting')
        # Test that at least one of context or target_language is given
        raises(TypeError, translate, 'short_greeting', context=None)
    
    def testSimpleFallbackTranslation(self):
        translate = self._service.translate
        raises = self.assertRaises
        eq = self.assertEqual
        # Test that a translation in an unsupported language returns a
        # translation in the fallback language (by default, English)
        eq(translate('default', 'short_greeting', target_language='es'),
           u'Hello!')
        # Same test, but use the context argument instead of target_language
        context = Environment()
        eq(translate('default', 'short_greeting', context=context),
           u'Hello!')


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(TestGlobalTranslationService)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
