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
"""

$Id: test_negotiator.py,v 1.7 2004/02/27 17:48:43 sidnei Exp $
"""
import unittest

from zope.i18n.negotiator import Negotiator
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.component.tests.placelesssetup import PlacelessSetup
from zope.interface import implements

class Env:
    implements(IUserPreferredLanguages)

    def __init__(self, langs=()):
        self.langs = langs

    def getPreferredLanguages(self):
        return self.langs


class NegotiatorTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(NegotiatorTest, self).setUp()
        self.Negotiator = Negotiator()

    def test1(self):

        _cases = (
            (('en','de'), ('en','de','fr'),  'en'),
            (('en'),      ('it','de','fr'),  None),
            (('pt-br','de'), ('pt_BR','de','fr'),  'pt_BR'),
            (('pt-br','en'), ('pt','en','fr'),  'en'),
            )

        for user_pref_langs, obj_langs, expected in _cases:
            env = Env(user_pref_langs)
            self.assertEqual(self.Negotiator.getLanguage(obj_langs, env),
                             expected)


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(NegotiatorTest)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
