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
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.tests import test_imessagecatalog


class TestPlurals(unittest.TestCase):

    def _getMessageCatalog(self, locale, variant="default"):
        path = os.path.dirname(tests.__file__)
        self._path = os.path.join(path, '%s-%s.mo' % (locale, variant))
        catalog = GettextMessageCatalog(locale, variant, self._path)
        return catalog

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
                         "Istnieją 0 plików.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         "Istnieje 1 plik.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         "Istnieją 3 pliki.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 17),
                         "Istnieją 17 plików.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 23),
                         "Istnieją 23 pliki.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 28),
                         "Istnieją 28 plików.")

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
