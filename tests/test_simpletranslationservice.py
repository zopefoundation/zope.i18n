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

$Id: test_simpletranslationservice.py,v 1.3 2003/03/25 23:25:15 bwarsaw Exp $
"""
import unittest
from zope.i18n.simpletranslationservice import SimpleTranslationService
from zope.i18n.tests.test_itranslationservice import TestITranslationService


class TestSimpleTranslationService(TestITranslationService):

    def _getTranslationService(self):
        service = SimpleTranslationService(
            {('default', 'en', 'short_greeting'): 'Hello!',
             ('default', 'de', 'short_greeting'): 'Hallo!',
             ('default', 'en', 'greeting'): 'Hello $name, how are you?',
             ('default', 'de', 'greeting'): 'Hallo $name, wie geht es Dir?'}
            )
        return service


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(TestSimpleTranslationService)

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
