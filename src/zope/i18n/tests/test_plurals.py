# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test a gettext implementation of a Message Catalog.
"""
import os
import unittest
from zope.i18n import tests
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18nmessageid import MessageFactory


class TestPlurals(unittest.TestCase):

    def _getMessageCatalog(self, locale, variant="default"):
        path = os.path.dirname(tests.__file__)
        self._path = os.path.join(path, '%s-%s.mo' % (locale, variant))
        catalog = GettextMessageCatalog(locale, variant, self._path)
        return catalog

    def _getTranslationDomain(self, locale, variant="default"):
        path = os.path.dirname(tests.__file__)
        self._path = os.path.join(path, '%s-%s.mo' % (locale, variant))
        catalog = GettextMessageCatalog(locale, variant, self._path)
        domain = TranslationDomain('default')
        domain.addCatalog(catalog)
        return domain

    def test_GermanPlurals(self):
        """Germanic languages such as english and german share the plural
        rule. We test the german here.
        """
        catalog = self._getMessageCatalog('de')
        self.assertEqual(catalog.language, 'de')

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         'Es gibt eine Datei.')
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         'Es gibt 3 Dateien.')
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 0),
                         'Es gibt 0 Dateien.')

        # Unknown id
        self.assertRaises(KeyError, catalog.getPluralMessage,
                          'There are %d files.', 'bar', 6)

        # Query without default values
        self.assertEqual(catalog.queryPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         'Es gibt eine Datei.')
        self.assertEqual(catalog.queryPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         'Es gibt 3 Dateien.')

        # Query with default values
        self.assertEqual(catalog.queryPluralMessage(
                         'There are %d files.', 'There is one file.', 1,
                         'Es gibt 1 Datei.', 'Es gibt %d Dateien !', ),
                         'Es gibt 1 Datei.')
        self.assertEqual(catalog.queryPluralMessage(
                         'There are %d files.', 'There is one file.', 3,
                         'Es gibt 1 Datei.', 'Es gibt %d Dateien !', ),
                         'Es gibt 3 Dateien !')

    def test_PolishPlurals(self):
        """Polish has a complex rule for plurals. It makes for a good
        test subject.
        """
        catalog = self._getMessageCatalog('pl')
        self.assertEqual(catalog.language, 'pl')

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 0),
                         u"Istnieją 0 plików.")
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         u"Istnieje 1 plik.")
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         u"Istnieją 3 pliki.")
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 17),
                         u"Istnieją 17 plików.")
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 23),
                         u"Istnieją 23 pliki.")
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 28),
                         u"Istnieją 28 plików.")

    def test_floater(self):
        """Test with the number being a float.
        We can use %f or %s to make sure it works.
        """
        catalog = self._getMessageCatalog('en')
        self.assertEqual(catalog.language, 'en')

        # It's cast to integer because of the %d in the translation string.
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1.0),
                         'There is one file.')
        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3.5),
                         'There are 3 files.')

        # It's cast to a string because of the %s in the translation string.
        self.assertEqual(catalog.getPluralMessage(
            'The item is rated 1/5 star.',
            'The item is rated %s/5 stars.', 3.5),
                         'The item is rated 3.5/5 stars.')

        # It's cast either to an int or a float because of the %s in
        # the translation string.
        self.assertEqual(catalog.getPluralMessage(
            'There is %d chance.',
            'There are %f chances.', 1.5),
                         'There are 1.500000 chances.')
        self.assertEqual(catalog.getPluralMessage(
            'There is %d chance.',
            'There are %f chances.', 3.5),
                         'There are 3.500000 chances.')

    def test_recursive_translation(self):
        domain = self._getTranslationDomain('en')
        factory = MessageFactory('default')
        translate = domain.translate

        # Singular
        banana = factory('banana', msgid_plural='bananas', number=1)
        phrase = factory('There is %d ${type}.',
                         msgid_plural='There are %d ${type}.',
                         number=1, mapping={'type': banana})
        self.assertEqual(
            translate(phrase, target_language="en"),
            'There is 1 banana.')

        # Plural
        apple = factory('apple', msgid_plural='apples', number=10)
        phrase = factory('There is %d ${type}.',
                         msgid_plural='There are %d ${type}.',
                         number=10, mapping={'type': apple})
        self.assertEqual(
            translate(phrase, target_language="en"),
            'There are 10 apples.')

        # Straight translation with translatable mapping
        apple = factory('apple', msgid_plural='apples', number=75)
        self.assertEqual(
            translate(msgid='There is %d ${type}.',
                      msgid_plural='There are %d ${type}.',
                      mapping={'type': apple},
                      target_language="en", number=75),
            'There are 75 apples.')

        # Add another catalog, to test the domain's catalogs iteration
        # We add this catalog in first position, to resolve the translations
        # there first.
        alt_en = self._getMessageCatalog('en', variant="alt")
        domain._data[alt_en.getIdentifier()] = alt_en
        domain._catalogs[alt_en.language].insert(0, alt_en.getIdentifier())

        apple = factory('apple', msgid_plural='apples', number=42)
        self.assertEqual(
            translate(msgid='There is %d ${type}.',
                      msgid_plural='There are %d ${type}.',
                      mapping={'type': apple},
                      target_language="de", number=42),
            'There are 42 oranges.')
