##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTLAR PURPOSE.
#
##############################################################################
"""Testing all XML Locale functionality.

$Id: test_xmllocales.py,v 1.5 2003/03/25 14:48:02 srichter Exp $
"""
import os
from unittest import TestCase, TestSuite, makeSuite

from zope.i18n.locales import XMLLocaleFactory
from zope.i18n.format import parseDateTimePattern, parseNumberPattern

class LocaleXMLFileTestCase(TestCase):
    """This test verifies that every locale XML fiel can be loaded."""

    def __init__(self, path):
        self.__path = path
        TestCase.__init__(self)
        
    # For unittest.
    def shortDescription(self):
        filename = os.path.split(self.__path)[-1]
        return '%s (Test  XML-Locale Files)' %filename

    def runTest(self):
        # Loading Locale object 
        locale = XMLLocaleFactory(self.__path)()

        # Making sure all number format patterns parse
        for klass in locale.getNumberFormatClasses():
            format = locale.getNumberFormat(klass)
            for id in format.getAllPatternIds():
                self.assert_(
                    parseNumberPattern(format.getPattern(id)) is not None)

        # Making sure all datetime patterns parse
        for calendar in locale.calendars.values():
            for pattern in calendar.datePatterns.values():
                    self.assert_(parseDateTimePattern(pattern) is not None)
            for pattern in calendar.timePatterns.values():
                    self.assert_(parseDateTimePattern(pattern) is not None)
                    

def test_suite():
    suite = TestSuite()
    from zope import i18n
    locale_dir = os.path.join(os.path.dirname(i18n.__file__), 'locales')
    for file in filter(lambda f: f.endswith('.xml'),
                       os.listdir(locale_dir))[:]:
        path = os.path.join(locale_dir, file)
        case = LocaleXMLFileTestCase(path)
        suite.addTest(case)
    return suite

# Note: These tests are disabled, just because they take a long time to run.
#       You should run these tests if you update the parsing code and/or
#       update the Locale XML Files.
def test_suite():
    return TestSuite((makeSuite(LocaleXMLFileTestCase),))
