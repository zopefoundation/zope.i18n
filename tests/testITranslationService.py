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
"""This is an 'abstract' test for the ITranslationService interface.

$Id: testITranslationService.py,v 1.2 2002/06/12 18:38:58 srichter Exp $
"""

import unittest
from Interface.Verify import verifyObject
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.App.ComponentArchitecture.metaConfigure import \
     provideService, managerHandler
from Zope.I18n.Negotiator import negotiator
from Zope.I18n.INegotiator import INegotiator
from Zope.I18n.IUserPreferredLanguages import IUserPreferredLanguages
from Zope.I18n.ITranslationService import ITranslationService
from Zope.I18n.IDomain import IDomain


class Environment:

    __implements__ = IUserPreferredLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getPreferredLanguages(self):
        return self.langs



class TestITranslationService(PlacelessSetup, unittest.TestCase):


    # This should be overwritten by every clas that inherits this test
    def _getTranslationService(self):
        pass
    

    def setUp(self):
        PlacelessSetup.setUp(self)
        self._service = self._getTranslationService() 
        assert verifyObject(ITranslationService, self._service)

        # Setup the negotiator service registry entry
        managerHandler('defineService', 'LanguageNegotiation', INegotiator) 
        provideService('LanguageNegotiation', negotiator, 'Zope.Public')
        

    # I know, I know. This is not part of the interface, but it is implemented
    # in every Translation Service, so it fits well here.
    def testInterpolation(self):
        service = self._service
        mapping = {'name': 'Zope', 'version': '3x'}

        self.assertEqual(service.interpolate(
            'This is $name.', mapping),
                         'This is Zope.')
        self.assertEqual(service.interpolate(
            'This is ${name}.', mapping),
                         'This is Zope.')
        self.assertEqual(service.interpolate(
            'This is $name version $version.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is ${name} version $version.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is $name version ${version}.', mapping),
                         'This is Zope version 3x.')
        self.assertEqual(service.interpolate(
            'This is ${name} version ${version}.', mapping),
                         'This is Zope version 3x.')
        

    def testSimpleNoTranslate(self):
        service = self._service
        self.assertRaises(TypeError, service.translate, 'Hello')
    
        self.assertEqual(service.translate('default', 'short_greeting',
                                           target_language='es'),
                         'short_greeting')

        context = Environment()
        self.assertEqual(service.translate('default', 'short_greeting',
                                           context=context),
                         'short_greeting')
    
        self.assertRaises(TypeError, service.translate, 'short_greeting',
                          context=None)
    
    
    def testSimpleTranslate(self):
        service = self._service
        self.assertEqual(service.translate('default', 'short_greeting',
                                           target_language='de'),
                         'Hallo!')

    
    def testDynamicTranslate(self):
        service = self._service    
        self.assertEqual(service.translate('default', 'greeting',
                                           mapping={'name': 'Stephan'},
                                           target_language='de'),
                         'Hallo Stephan, wie geht es Dir?')
        

    def testGetDomain(self):
        service = self._service    
        domain = service.getDomain('default')
        self.assertEqual(verifyObject(IDomain, domain), 1)

        
def test_suite():
    pass
