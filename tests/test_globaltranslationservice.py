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

$Id: test_globaltranslationservice.py,v 1.5 2003/03/25 23:25:15 bwarsaw Exp $
"""
import unittest, sys, os
from zope.i18n.globaltranslationservice import GlobalTranslationService
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.tests.test_itranslationservice import \
     TestITranslationService, Environment
from zope.i18n import MessageIDFactory

def testdir():
    from zope.i18n import tests
    return os.path.dirname(tests.__file__)


class TestGlobalTranslationService(TestITranslationService):

    def _getTranslationService(self):
        service = GlobalTranslationService('default')
        path = testdir()
        en_catalog = GettextMessageCatalog('en', 'default',
                                           os.path.join(path, 'en-default.mo'))
        de_catalog = GettextMessageCatalog('de', 'default',
                                           os.path.join(path, 'de-default.mo'))
        alt_en_catalog = GettextMessageCatalog('en', 'alt',
                                               os.path.join(path, 'en-alt.mo'))
        service.addCatalog(alt_en_catalog)
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


    def testStringTranslate(self):
        translate = self._service.translate
        self.assertEqual(translate('default', u'short_greeting',
                                   target_language='en'),
                         u'Hello!')

    def testMessageIDTranslate(self):
        translate = self._service.translate
        self.assertEqual(translate('default', u'short_greeting',
                                   target_language='en'),
                         u'Hello!')
        msgid = MessageIDFactory('alt')('short_greeting')
        self.assertEqual(translate('default', msgid,
                                   target_language='en'),
                         u'Hey!')


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
