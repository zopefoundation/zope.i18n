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
"""This module tests the LocaleProvider and everything that goes with it.

$Id: test_locales.py,v 1.6 2003/04/30 23:37:59 faassen Exp $
"""
import os
import datetime
from unittest import TestCase, TestSuite, makeSuite

from zope.i18n.interfaces import ILocaleProvider, ILocale
from zope.i18n.interfaces import ILocaleVersion, ILocaleIdentity
from zope.i18n.interfaces import ILocaleTimeZone, ILocaleCalendar
from zope.i18n.interfaces import ILocaleNumberFormat, ILocaleCurrency

from zope.i18n.locales import LoadLocaleError
from zope.i18n.locales import LocaleProvider, XMLLocaleFactory
from zope.i18n.locales import locales
from zope.i18n.locales import LocaleVersion, LocaleIdentity
from zope.i18n.locales import LocaleTimeZone, LocaleCalendar
from zope.i18n.locales import LocaleNumberFormat, LocaleCurrency

from zope.i18n import tests
testdir = os.path.dirname(tests.__file__)

class TestILocaleProvider(TestCase):
    """Test the functionality of an implmentation of the ILocaleProvider
    interface."""

    def _makeNewProvider(self):
        raise NotImplemented

    def setUp(self):
        self.locales = self._makeNewProvider()

    def testInterfaceConformity(self):
        self.assert_(ILocaleProvider.isImplementedBy(self.locales))

    def test_getLocale(self):
        locale = self.locales.getLocale(None, None, None)
        self.assertEqual(locale.id.language, None)
        self.assertEqual(locale.id.country, None)
        self.assertEqual(locale.id.variant, None)

        locale = self.locales.getLocale('de', None, None)
        self.assertEqual(locale.id.language, 'de')
        self.assertEqual(locale.id.country, None)
        self.assertEqual(locale.id.variant, None)

        locale = self.locales.getLocale('de', 'DE', None)
        self.assertEqual(locale.id.language, 'de')
        self.assertEqual(locale.id.country, 'DE')
        self.assertEqual(locale.id.variant, None)

        locale = self.locales.getLocale('de', 'DE', 'PREEURO')
        self.assertEqual(locale.id.language, 'de')
        self.assertEqual(locale.id.country, 'DE')
        self.assertEqual(locale.id.variant, 'PREEURO')


class TestLocaleProvider(TestILocaleProvider):

    def _makeNewProvider(self):
        return LocaleProvider(os.path.join(testdir, 'xmllocales'))

    def test_loadLocale(self):
        self.locales.loadLocale(None, None, None)
        self.assertEqual(self.locales._locales.keys(), [(None, None, None)])

        self.locales.loadLocale('de', None, None)
        self.assert_(('de', None, None) in self.locales._locales.keys())

    def test_loadLocaleFailure(self):
        self.assertRaises(LoadLocaleError, self.locales.loadLocale, 'xxx')


class TestLocaleIdentity(TestCase):

    def setUp(self):
        self.id = LocaleIdentity('de', 'DE', 'PREEURO')
        self.id2 = LocaleIdentity()

    def testInterfaceConformity(self):
        self.assert_(ILocaleIdentity.isImplementedBy(self.id))

    def test_language(self):
        self.assertEqual(self.id.language, 'de')
        self.assertEqual(self.id2.language, None)

    def test_country(self):
        self.assertEqual(self.id.country, 'DE')
        self.assertEqual(self.id2.country, None)

    def test_variant(self):
        self.assertEqual(self.id.variant, 'PREEURO')
        self.assertEqual(self.id2.variant, None)

    def test___repr__(self):
        self.assertEqual(self.id.__repr__(),
                         "<LocaleIdentity (de, DE, PREEURO)>")
        self.assertEqual(self.id2.__repr__(),
                         "<LocaleIdentity (None, None, None)>")

class TestLocaleVersion(TestCase):

    def setUp(self):
        self.ver = LocaleVersion('1.0',
                                    datetime.datetime(2003, 01, 01, 12, 00),
                                    'Initial data set.')
        self.ver2 = LocaleVersion('2.0',
                                     datetime.datetime(2003, 01, 02, 12, 00),
                                     'Made some changes.')

    def testInterfaceConformity(self):
        self.assert_(ILocaleVersion.isImplementedBy(self.ver))
        self.assert_(ILocaleVersion.isImplementedBy(self.ver2))

    def test_id(self):
        self.assertEqual(self.ver.id,  '1.0')
        self.assertEqual(self.ver2.id, '2.0')

    def test_date(self):
        self.assertEqual(self.ver.date,
                         datetime.datetime(2003, 01, 01, 12, 00))
        self.assertEqual(self.ver2.date,
                         datetime.datetime(2003, 01, 02, 12, 00))

    def test_comment(self):
        self.assertEqual(self.ver.comment,  'Initial data set.')
        self.assertEqual(self.ver2.comment, 'Made some changes.')

    def test___cmp__(self):
        self.assert_(self.ver < self.ver2)
        self.assert_(self.ver2 > self.ver)
        self.assert_(self.ver2 != self.ver)


class TestLocaleTimeZone(TestCase):

    def setUp(self):
        self.tz = LocaleTimeZone('Europe/Berlin')

    def testInterfaceConformity(self):
        self.assert_(ILocaleTimeZone.isImplementedBy(self.tz))

    def testId(self):
        self.assertEqual(self.tz.id, 'Europe/Berlin')


class TestLocaleCalendar(TestCase):

    def setUp(self):
        self.cal = LocaleCalendar('gregorian')
        self.cal.months = {1: ('January', 'Jan')}
        self.cal.weekdays = {1: ('Sunday', 'Su')}
        self.cal.eras = {0: 'B.C.'}
        self.cal.am = 'AM'
        self.cal.pm = 'PM'
        self.cal.patternCharacters = 'GjMtkHmsSEDFwWahKzJe'
        self.cal.timePatterns = {'medium': 'HH:mm:ss'}
        self.cal.datePatterns = {'medium': 'dd.MM.yyyy'}
        self.cal.datetimePattern = '{1} {0}'

    def testInterfaceConformity(self):
        self.assert_(ILocaleCalendar.isImplementedBy(self.cal))

    def test_getMonthNames(self):
        self.cal.months[2] = ('February', 'Feb')
        self.assertEqual(self.cal.getMonthNames(),
                         ['January', 'February'] + [None]*10)

    def test_getMonthIdFromName(self):
        self.assertEqual(self.cal.getMonthIdFromName('January'), 1)

    def test_getMonthAbbr(self):
        self.cal.months[2] = ('February', 'Feb')
        self.assertEqual(self.cal.getMonthAbbr(), ['Jan', 'Feb'] + [None]*10)

    def test_getMonthIdFromAbbr(self):
        self.assertEqual(self.cal.getMonthIdFromAbbr('Jan'), 1)

    def test_getWeekdayNames(self):
        self.cal.weekdays[2] = ('Monday', 'Mo')
        self.assertEqual(self.cal.getWeekdayNames(),
                         ['Sunday', 'Monday'] + [None]*5)

    def test_getWeekdayIdFromName(self):
        self.assertEqual(self.cal.getWeekdayIdFromName('Sunday'), 1)

    def test_getWeekdayAbbr(self):
        self.cal.weekdays[2] = ('Monday', 'Mo')
        self.assertEqual(self.cal.getWeekdayAbbr(), ['Su', 'Mo'] + [None]*5)

    def test_getWeekdayIdFromAbbr(self):
        self.assertEqual(self.cal.getWeekdayIdFromAbbr('Su'), 1)


class TestLocaleNumberFormat(TestCase):

    def setUp(self):
        self.format = LocaleNumberFormat('decimal')
        self.format.patterns = {'decimal': '#,##0.###;-#,##0.###'}
        self.format.symbols = {'decimal': '.'}

    def testInterfaceConformity(self):
        self.assert_(ILocaleNumberFormat.isImplementedBy(self.format))


class TestLocaleCurrency(TestCase):

    def setUp(self):
        self.curr = LocaleCurrency('USD')
        self.curr.symbol = '$'
        self.curr.name = 'USD'
        self.curr.decimal = '.'
        self.curr.pattern = '$ #,##0.00;-$ #,##0.00'

    def testInterfaceConformity(self):
        self.assert_(ILocaleCurrency.isImplementedBy(self.curr))


class TestXMLLocaleFactory(TestCase):

    factory0 = XMLLocaleFactory(
        os.path.join(testdir, 'xmllocales', 'root.xml'))
    factory = XMLLocaleFactory(
        os.path.join(testdir, 'xmllocales', 'de.xml'))
    factory2 = XMLLocaleFactory(
        os.path.join(testdir, 'xmllocales', 'de_DE.xml'))
    factory3 = XMLLocaleFactory(
        os.path.join(testdir, 'xmllocales', 'de_DE_PREEURO.xml'))

    def test_GermanySpecificGermanLocale(self):
        # Well, if the factory can create the Locale we are in good
        # shape. This test is only suppose to test whether XML-files with
        # missing elements cane also be handled by the factory.
        locale = self.factory0()
        self.assert_(ILocale.isImplementedBy(locale))
        locale = self.factory2()
        self.assert_(ILocale.isImplementedBy(locale))
        locale = self.factory3()
        self.assert_(ILocale.isImplementedBy(locale))


    def test_extractIdentity(self):
        id = self.factory._extractIdentity()
        self.assertEqual(id.language, 'de')
        self.assertEqual(id.variant, None)
        self.assertEqual(id.country, None)
        self.assertEqual(id.correspondsTos, [(u'0007', u'Windows')])
        self.assertEqual(id.__repr__(), '<LocaleIdentity (de, None, None)>')

    def test_extractVersions(self):
        versions = self.factory._extractVersions()
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0].id, u'1.0')
        self.assertEqual(versions[0].date,
                         datetime.datetime(2002, 6, 11, 15, 6, 8))
        self.assertEqual(versions[0].comment,
                         u'Various notes and changes in version 1.0')

    def test_extractLanguages(self):
        langs = self.factory._extractLanguages()
        self.assertEqual(len(langs), 83)
        self.assertEqual(langs['de'], 'Deutsch')
        self.assertEqual(langs['ab'], 'Abchasisch')
        self.assertEqual(langs['zh'], 'Chinesisch')

    def test_extractCountries(self):
        countries = self.factory._extractCountries()
        self.assertEqual(len(countries), 145)
        self.assertEqual(countries['DE'], 'Deutschland')
        self.assertEqual(countries['AE'], 'Vereinigte Arabische Emirate')
        self.assertEqual(countries['ZW'], 'Simbabwe')

    def test_extractTimeZones(self):
        zones = self.factory._extractTimeZones()
        self.assertEqual(len(zones), 1)
        zone = zones[0]
        self.assertEqual(zone[0], u'Europe/Berlin')
        self.assertEqual(zone[0], zone[1].id)
        self.assertEqual(zone[1].cities, [u'Berlin'])
        self.assertEqual(zone[1].names['generic'],
                         (u'Mitteleurop\xe4ische Zeit', u'Europe/Berlin'))
        self.assertEqual(zone[2], True)

    def test_extractCalendars(self):
        cals = self.factory._extractCalendars()
        self.assertEqual(len(cals), 1)
        cal = cals[0]
        self.assertEqual(cal[0], u'gregorian')
        self.assertEqual(cal[0], cal[1].klass)
        self.assertEqual(cal[1].months[1], (u'Januar', u'Jan'))
        self.assertEqual(cal[1].weekdays[1], (u'Sonntag', u'So'))
        self.assertEqual(cal[2], True)

    def test_extractNumberFormats(self):
        formats = self.factory0._extractNumberFormats()
        self.assertEqual(len(formats), 1)
        format = formats[0]
        self.assertEqual(format[0], u'decimal')
        self.assertEqual(format[0], format[1].klass)
        self.assertEqual(format[1].patterns['decimal'],
                         '#,##0.###;-#,##0.###')
        self.assertEqual(format[1].patterns['percent'], '#,##0%')
        self.assertEqual(format[1].patterns['scientific'], '#E0')
        self.assertEqual(format[1].symbols['percentSign'], u'%')
        self.assertEqual(format[1].symbols['nativeZeroDigit'], u'0')
        self.assertEqual(format[1].symbols['exponential'], u'E')
        self.assertEqual(format[1].symbols['perMille'], u'\u2030')
        self.assertEqual(format[2], True)

    def test_extractCurrencies(self):
        currs = self.factory3._extractCurrencies()
        self.assertEqual(len(currs), 1)
        curr = currs[0]
        self.assertEqual(curr[0], u'DEM')
        self.assertEqual(curr[0], curr[1].id)
        self.assertEqual(curr[1].symbol, u'DM')
        self.assertEqual(curr[1].name, u'DEM')
        self.assertEqual(curr[1].decimal, u',')
        self.assertEqual(curr[1].pattern, None)
        self.assertEqual(curr[2], True)


class TestLocale(TestCase):

    path = os.path.join(testdir, 'xmllocales', 'root.xml')
    localeFactory = XMLLocaleFactory(path)
    locale = localeFactory()

    def testId(self):
        id = self.locale.id
        self.assertEqual(id.language, None)
        self.assertEqual(id.variant, None)
        self.assertEqual(id.country, None)
        self.assertEqual(id.correspondsTos, [(u'0000', u'Windows')])

    def test_getLatestVersion(self):
        self.assertEqual(self.locale.getLatestVersion().id, u'1.0')

    def test_getDefaultTimeZone(self):
        zone = self.locale.getDefaultTimeZone()
        self.assertEqual(zone.id, u'PST')

    def test_getDefaultCalendar(self):
        cal = self.locale.getDefaultCalendar()
        self.assertEqual(cal.klass, u'gregorian')

    def test_getDefaultNumberFormat(self):
        format = self.locale.getDefaultNumberFormat()
        self.assertEqual(format.klass, u'decimal')

    def test_getDefaultCurrency(self):
        curr = self.locale.getDefaultCurrency()
        self.assertEqual(curr.id, u'XXX')


class TestLocaleAndProvider(TestCase):

    # Set the locale on the class so that test cases don't have
    # to pay to construct a new one each time.

    orig = locales._locale_dir
    locales._locale_dir = os.path.join(testdir, 'xmllocales')
    locales.loadLocale(None, None, None)
    locales.loadLocale('de', None, None)
    locales.loadLocale('de', 'DE', None)
    locales.loadLocale('de', 'DE', 'PREEURO')
    locale = locales.getLocale('de', 'DE', 'PREEURO')
    locales._locale_dir = orig

    def test_getDisplayLanguage(self):
        self.assertEqual(self.locale.getDisplayLanguage('de'), 'Deutsch')
        self.assertRaises(KeyError, self.locale.getDisplayLanguage,
                    ('xx',))

    def test_getDisplayCountry(self):
        self.assertEqual(self.locale.getDisplayCountry('DE'), 'Deutschland')
        self.assertRaises(KeyError, self.locale.getDisplayCountry,
                    ('XX',))

    def test_getTimeFormatter(self):
        formatter = self.locale.getTimeFormatter('medium')
        self.assertEqual(formatter.getPattern(), 'HH:mm:ss')
        self.assertEqual(formatter.format(datetime.time(12, 30, 10)),
                         '12:30:10')
        self.assertEqual(formatter.parse('12:30:10'),
                         datetime.time(12, 30, 10))

    def test_getDateFormatter(self):
        formatter = self.locale.getDateFormatter('medium')
        self.assertEqual(formatter.getPattern(), 'dd.MM.yyyy')
        self.assertEqual(formatter.format(datetime.date(2003, 01, 02)),
                         '02.01.2003')
        self.assertEqual(formatter.parse('02.01.2003'),
                         datetime.date(2003, 01, 02))

    def test_getDateTimeFormatter(self):
        formatter = self.locale.getDateTimeFormatter('medium')
        self.assertEqual(formatter.getPattern(), 'dd.MM.yyyy HH:mm:ss ')
        self.assertEqual(
            formatter.format(datetime.datetime(2003, 01, 02, 12, 30)),
            '02.01.2003 12:30:00 ')
        self.assertEqual(formatter.parse('02.01.2003 12:30:00 '),
                         datetime.datetime(2003, 01, 02, 12, 30))

    def test_getNumberFormatter(self):
        formatter = self.locale.getNumberFormatter('decimal')
        self.assertEqual(formatter.getPattern(), '#,##0.###;-#,##0.###')
        self.assertEqual(formatter.format(1234.5678), '1,234.567')
        self.assertEqual(formatter.format(-1234.5678), '-1,234.567')
        self.assertEqual(formatter.parse('1,234.567'), 1234.567)
        self.assertEqual(formatter.parse('-1,234.567'), -1234.567)


class TestGlobalLocaleProvider(TestCase):

    def testLoading(self):
        locales.loadLocale(None, None, None)
        self.assert_(locales._locales.has_key((None, None, None)))
        locales.loadLocale('de', None, None)
        self.assert_(locales._locales.has_key(('de', None, None)))
        locales.loadLocale('de', 'DE', None)
        self.assert_(locales._locales.has_key(('de', 'DE', None)))
        locales.loadLocale('de', 'DE', 'PREEURO')
        self.assert_(locales._locales.has_key(('de', 'DE', 'PREEURO')))

    def test_getLocale(self):
        locale = locales.getLocale('de', 'AT')
        self.assertEqual(locale.id.language, 'de')
        self.assertEqual(locale.id.country, 'AT')
        self.assertEqual(locale.id.variant, None)


def test_suite():
    return TestSuite((
        makeSuite(TestLocaleProvider),
        makeSuite(TestLocaleIdentity),
        makeSuite(TestLocaleVersion),
        makeSuite(TestLocaleTimeZone),
        makeSuite(TestLocaleCalendar),
        makeSuite(TestLocaleNumberFormat),
        makeSuite(TestLocaleCurrency),
        makeSuite(TestXMLLocaleFactory),
        makeSuite(TestLocale),
        makeSuite(TestLocaleAndProvider),
        makeSuite(TestGlobalLocaleProvider),
        ))
