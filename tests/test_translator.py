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

$Id: test_translator.py,v 1.9 2004/02/27 22:25:23 srichter Exp $
"""
import os
import unittest

from zope.component.tests.placelesssetup import PlacelessSetup
from zope.component import getServiceManager

from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.interfaces import ITranslationService, INegotiator
from zope.i18n.negotiator import negotiator
from zope.i18n.simpletranslationservice import SimpleTranslationService
from zope.i18n.tests.test_simpletranslationservice import data
from zope.i18n.tests.test_negotiator import Env as ContextStub
from zope.i18n.translate import Translator


class TranslatorTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(TranslatorTest, self).setUp()

        sm = getServiceManager(None)
        sm.defineService('Translation', ITranslationService)
        sm.provideService('Translation', SimpleTranslationService(data))

        sm.defineService('LanguageNegotiation', INegotiator)
        sm.provideService('LanguageNegotiation', negotiator)

    def test_translator(self):
        translator = Translator('default', ContextStub(['de']))
        self.assertEqual(translator.translate('short_greeting'),
                         'Hallo!')

        translator = Translator('default', ContextStub(['de']))
        self.assertEqual(translator.translate('short_greeting', default=42),
                         'Hallo!')

        translator = Translator('default', ContextStub(['es']))
        self.assertEqual(translator.translate('short_greeting', default=42),
                         42)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TranslatorTest),
                           ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
