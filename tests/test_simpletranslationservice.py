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

$Id: test_simpletranslationservice.py,v 1.5 2004/02/27 22:25:23 srichter Exp $
"""
import unittest
from zope.i18n.simpletranslationservice import SimpleTranslationService
from zope.i18n.tests.test_itranslationservice import TestITranslationService


data = {
    ('default', 'en', 'short_greeting'): 'Hello!',
    ('default', 'de', 'short_greeting'): 'Hallo!',
    ('default', 'en', 'greeting'): 'Hello $name, how are you?',
    ('default', 'de', 'greeting'): 'Hallo $name, wie geht es Dir?'}


class TestSimpleTranslationService(unittest.TestCase, TestITranslationService):

    def setUp(self):
        TestITranslationService.setUp(self)

    def _getTranslationService(self):
        service = SimpleTranslationService(data)
        return service


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSimpleTranslationService))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
