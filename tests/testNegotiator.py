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

$Id: testNegotiator.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""
import unittest, sys

from Zope.I18n.Negotiator import Negotiator
from Zope.I18n.IUserPreferedLanguages import IUserPreferedLanguages
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup

class Env:

    __implements__ = IUserPreferedLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getLanguages(self):
        return self.langs


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        PlacelessSetup.setUp(self)
        self.Negotiator= Negotiator()

    def test1(self):

        _cases = (
            ( ('en','de'),    ('en','de','fr'),  'en'),
            ( ('en'),         ('it','de','fr'),  None)
        )

        for user_pref_langs, obj_langs, expected in _cases:
        
            env = Env(user_pref_langs)

            self.assertEqual( self.Negotiator.getLanguage( obj_langs, env), 
                                expected) 

        


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
