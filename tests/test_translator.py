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

$Id: test_translator.py,v 1.5 2003/05/01 19:35:43 faassen Exp $
"""

import os
import unittest

from zope.i18n.interfaces import ILocaleIdentity, ILocale
from zope.i18n.translate import Translator
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.tests.test_globaltranslationservice import testdir
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.component import getService

class LocaleIdentityStub:
    # Lie -- we're only going to implement part of the interface
    __implements__ = ILocaleIdentity

    def __init__(self, language=None):
        self.language = language

class LocaleStub:
    # Lie -- we're only going to implement part of the interface
    __implements__ = ILocale

    def __init__(self, language=None):
        self.id = LocaleIdentityStub(language)


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

    def test_translator(self):
        locale = LocaleStub('de')
        translator = Translator(locale, 'default', None)
        self.assertEqual(translator.translate('short_greeting'), 'Hallo!')

        # context is something that is not adaptable to IUserPreferredLanguages
        context = object()
        locale = LocaleStub(None)
        translator = Translator(locale, 'default', context)
        self.assertEqual(translator.translate('short_greeting', default=42), 42)



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TranslatorTests))
    return suite
