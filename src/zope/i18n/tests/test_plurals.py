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
                         "Istnieją 0 pliko'w.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 1),
                         "Istnieje 1 plik.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 3),
                         "Istnieją 3 pliki.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 17),
                         "Istnieją 17 pliko'w.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 23),
                         "Istnieją 23 pliki.")

        self.assertEqual(catalog.getPluralMessage(
                         'There is one file.', 'There are %d files.', 28),
                         "Istnieją 28 pliko'w.")


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestPlurals),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
