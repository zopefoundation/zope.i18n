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

$Id: testIReadTranslationService.py,v 1.2 2002/06/18 18:23:56 bwarsaw Exp $
"""

import unittest
from Interface.Verify import verifyObject
from Zope.ComponentArchitecture.tests.PlacelessSetup import PlacelessSetup
from Zope.App.ComponentArchitecture.metaConfigure import \
     provideService, managerHandler
from Zope.I18n.Negotiator import negotiator
from Zope.I18n.INegotiator import INegotiator
from Zope.I18n.IUserPreferredLanguages import IUserPreferredLanguages
from Zope.I18n.ITranslationService import IReadTranslationService
from Zope.I18n.IDomain import IDomain


class Environment:

    __implements__ = IUserPreferredLanguages

    def __init__(self, langs=()):
        self.langs = langs

    def getPreferredLanguages(self):
        return self.langs



class TestIReadTranslationService(PlacelessSetup, unittest.TestCase):

    # This should be overwritten by every clas that inherits this test
    def _getTranslationService(self):
        pass
    
    def setUp(self):
        PlacelessSetup.setUp(self)
        self._service = self._getTranslationService() 
        assert verifyObject(IReadTranslationService, self._service)
        # Setup the negotiator service registry entry
        managerHandler('defineService', 'LanguageNegotiation', INegotiator) 
        provideService('LanguageNegotiation', negotiator, 'Zope.Public')

    # I know, I know. This is not part of the interface, but it is implemented
    # in every Translation Service, so it fits well here.
    def testInterpolation(self):
        service = self._service
        interp = service.interpolate
        eq = self.assertEqual
        mapping = {'name': 'Zope', 'version': '3x'}
        # Test simple interpolations
        eq(interp('This is $name.', mapping), 'This is Zope.')
        eq(interp('This is ${name}.', mapping), 'This is Zope.')
        # Test more than one interpolation variable
        eq(interp('This is $name version $version.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is ${name} version $version.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is $name version ${version}.', mapping),
           'This is Zope version 3x.')
        eq(interp('This is ${name} version ${version}.', mapping),
           'This is Zope version 3x.')
        # Test escaping the $
        eq(interp('This is $$name.', mapping), 'This is $$name.')
        eq(interp('This is $${name}.', mapping), 'This is $${name}.')
        
    def testSimpleTranslate(self):
        translate = self._service.translate
        eq = self.assertEqual
        # Test that a given message id is properly translated in a supported
        # language
        eq(translate('default', 'short_greeting', target_language='de'),
           'Hallo!')
        # Same test, but use the context argument
        context = Environment(('de', 'en'))
        eq(translate('default', 'short_greeting', context=context),
           'Hallo!')
    
    def testDynamicTranslate(self):
        translate = self._service.translate
        eq = self.assertEqual
        # Testing both translation and interpolation
        eq(translate('default', 'greeting', mapping={'name': 'Stephan'},
                     target_language='de'),
           'Hallo Stephan, wie geht es Dir?')

    def testGetDomain(self):
        service = self._service    
        domain = service.getDomain('default')
        self.assertEqual(verifyObject(IDomain, domain), 1)

    def testDomainTranslate(self):
        service = self._service    
        domain = service.getDomain('default')
        translate = domain.translate
        eq = self.assertEqual
        # target language argument
        eq(translate('short_greeting', target_language='de'), 'Hallo!')
        # context argument
        context = Environment(('de', 'en'))
        eq(translate('short_greeting', context=context), 'Hallo!')
        
def test_suite():
    pass
