##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""This module tests the ITranslator / Translator

$Id: test_translator.py,v 1.3 2003/03/25 23:25:15 bwarsaw Exp $
"""

import os
import unittest

from zope.i18n.globaltranslationservice import GlobalTranslationService
from zope.i18n.interfaces import ITranslationService
from zope.i18n.interfaces import ILocaleIdentity, ILocale
from zope.i18n.translate import Translator
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.tests.test_globaltranslationservice import testdir
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component import getService


class TranslatorTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        # Create all the goo for placeless services
        PlacelessSetup.setUp(self)
        # Create a global translation service, initialized with a bunch of
        # catalogs (stolen from test_globaltranslationservice.py).
        path = testdir()
        de_catalog = GettextMessageCatalog('de', 'default',
                                           os.path.join(path, 'de-default.mo'))
        service = getService(None, 'Translation')
        service.addCatalog(de_catalog)

        # Create a stub ILocaleIdentity
        class LocaleIdentityStub:
            # Lie -- we're only going to implement part of the interface
            __implements__ = ILocaleIdentity
            language = 'de'

        # Create a stub ILocale
        class LocaleStub:
            # Lie -- we're only going to implement part of the interface
            __implements__ = ILocale
            id = LocaleIdentityStub()

        self._locale = LocaleStub()

    def test_translator(self):
        translator = Translator(self._locale, 'default', None)
        self.assertEqual(translator.translate('short_greeting'), 'Hallo!')



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TranslatorTests))
    return suite
