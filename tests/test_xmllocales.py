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
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Testing all XML Locale functionality.

$Id: test_xmllocales.py,v 1.2 2003/01/06 09:24:45 srichter Exp $
"""
import os
from unittest import TestCase, TestSuite, makeSuite

from zope.i18n.locales import ICUXMLLocaleFactory
from zope.i18n.format import parseDateTimePattern, parseNumberPattern

class LocaleXMLFileTestCase(TestCase, object):
    """This test verifies that every locale XML fiel can be loaded."""

    def __init__(self, path):
        self.__path = path
        super(LocaleXMLFileTestCase, self).__init__()
        
    # For unittest.
    def shortDescription(self):
        filename = os.path.split(self.__path)[-1]
        return '%s (Test ICU XML-Locale Files)' %filename

    def runTest(self):
        # Loading Locale object 
        locale = ICUXMLLocaleFactory(self.__path)()

        # Making sure all number format patterns parse
        for klass in locale.getNumberFormatClasses():
            format = locale.getNumberFormat(klass)
            for id in format.getAllPatternIds():
                self.assert_(
                    parseNumberPattern(format.getPattern(id)) is not None)

        # Making sure all datetime patterns parse
        for klass in locale.getCalendarClasses():
            calendar = locale.getCalendar(klass)
            for pattern in calendar._date_patterns.values():
                    self.assert_(parseDateTimePattern(pattern) is not None)
            for pattern in calendar._time_patterns.values():
                    self.assert_(parseDateTimePattern(pattern) is not None)
                    

def test_suite():
    suite = TestSuite()
    from zope import i18n
    locale_dir = os.path.join(os.path.dirname(i18n.__file__), 'locales')
    org = os.curdir
    os.chdir(locale_dir)
    for file in filter(lambda f: f.endswith('.xml'),
                       os.listdir(locale_dir))[:]:
        path = os.path.join(locale_dir, file)
        case = LocaleXMLFileTestCase(path)
        suite.addTest(case)
    os.chdir(org)
    return suite
