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

$Id: test_locales.py,v 1.1 2003/01/05 20:20:21 srichter Exp $
"""
import os, sys
import datetime
from unittest import TestCase, TestSuite, makeSuite

from zope.i18n.interfaces import ILocaleProvider, ILocale 
from zope.i18n.interfaces import ILocaleVersion, ILocaleIdentity
from zope.i18n.interfaces import ILocaleTimeZone, ILocaleCalendar
from zope.i18n.interfaces import ILocaleNumberFormat, ILocaleCurrency

from zope.i18n.locales import NoGeneralLocaleError, LoadLocaleError
from zope.i18n.locales import LocaleProvider, ICULocale, ICUXMLLocaleFactory
from zope.i18n.locales import locales
from zope.i18n.locales import ICULocaleVersion, ICULocaleIdentity
from zope.i18n.locales import ICULocaleTimeZone, ICULocaleCalendar 
from zope.i18n.locales import ICULocaleNumberFormat, ICULocaleCurrency 

def testdir():
    from zope.i18n import tests
    return os.path.dirname(tests.__file__)


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
        self.assertEqual(locale.id.getLanguage(), None)
        self.assertEqual(locale.id.getCountry(), None)
        self.assertEqual(locale.id.getVariant(), None)

        locale = self.locales.getLocale('de', None, None)
        self.assertEqual(locale.id.getLanguage(), 'de')
        self.assertEqual(locale.id.getCountry(), None)
        self.assertEqual(locale.id.getVariant(), None)

        locale = self.locales.getLocale('de', 'DE', None)
        self.assertEqual(locale.id.getLanguage(), 'de')
        self.assertEqual(locale.id.getCountry(), 'DE')
        self.assertEqual(locale.id.getVariant(), None)

        locale = self.locales.getLocale('de', 'DE', 'PREEURO')
        self.assertEqual(locale.id.getLanguage(), 'de')
        self.assertEqual(locale.id.getCountry(), 'DE')
        self.assertEqual(locale.id.getVariant(), 'PREEURO')


class TestLocaleProvider(TestILocaleProvider):

    def _makeNewProvider(self):
        return LocaleProvider(os.path.join(testdir(), 'xmllocales'))

    def test_loadLocale(self):
        self.locales.loadLocale(None, None, None)
        self.assertEqual(self.locales._locales.keys(), [(None, None, None)])

        self.locales.loadLocale('de', None, None)
        self.assert_(('de', None, None) in self.locales._locales.keys())

    def test_loadLocaleFailure(self):
        self.assertRaises(LoadLocaleError, self.locales.loadLocale, 'xxx')


class TestICULocaleIdentity(TestCase):

    def setUp(self):
        self.id = ICULocaleIdentity('de', 'DE', 'PREEURO')
        self.id2 = ICULocaleIdentity()

    def testInterfaceConformity(self):
        self.assert_(ILocaleIdentity.isImplementedBy(self.id))

    def test_getLanguage(self):
        self.assertEqual(self.id.getLanguage(), 'de')
        self.assertEqual(self.id2.getLanguage(), None)

    def test_getCountry(self):
        self.assertEqual(self.id.getCountry(), 'DE')
        self.assertEqual(self.id2.getCountry(), None)

    def test_getVariant(self):
        self.assertEqual(self.id.getVariant(), 'PREEURO')
        self.assertEqual(self.id2.getVariant(), None)

    def test_setCorrespondence(self):
        self.id.setCorrespondence('0007', 'Windows')
        self.assertEqual(self.id._correspondsTos, [('0007', 'Windows')])

    def test_getAllCorrespondences(self):
        self.id.setCorrespondence('0007', 'Windows')
        self.id.setCorrespondence('de_plain', 'Fantasy')
        self.assertEqual(self.id.getAllCorrespondences(),
                         [('0007', 'Windows'), ('de_plain', 'Fantasy')])

    def test___repr__(self):
        self.assertEqual(self.id.__repr__(),
                         "<ICULocaleIdentity (de, DE, PREEURO)>")
        self.assertEqual(self.id2.__repr__(),
                         "<ICULocaleIdentity (None, None, None)>")

class TestICULocaleVersion(TestCase):

    def setUp(self):
        self.ver = ICULocaleVersion('1.0',
                                    datetime.datetime(2003, 01, 01, 12, 00),
                                    'Initial data set.')
        self.ver2 = ICULocaleVersion('2.0',
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


class TestICULocaleTimeZone(TestCase):

    def setUp(self):
        self.tz = ICULocaleTimeZone('Europe/Berlin')

    def testInterfaceConformity(self):
        self.assert_(ILocaleTimeZone.isImplementedBy(self.tz))

    def testId(self):
        self.assertEqual(self.tz.id, 'Europe/Berlin')

    def test_addCity_getCities(self):
        tz = self.tz
        tz.addCity('a')
        tz.addCity('b')
        self.assertEqual(list(tz.getCities()), ['a', 'b'])

    def test_setName_getName(self):
        tz = self.tz
        tz.setName(u'generic', u'Mitteleurop\xe4ische Zeit', u'Europe/Berlin')
        self.assertEqual(tz.getName(u'generic'),
                         (u'Mitteleurop\xe4ische Zeit', u'Europe/Berlin'))


class TestICULocaleCalendar(TestCase):

    def setUp(self):
        self.cal = ICULocaleCalendar('gregorian')
        self.cal._months = {1: ('January', 'Jan')}
        self.cal._weekdays = {1: ('Sunday', 'Su')}
        self.cal._eras = {0: 'B.C.'}
        self.cal._am = 'AM'
        self.cal._pm = 'PM'
        self.cal._pattern_chars = 'GjMtkHmsSEDFwWahKzJe'
        self.cal._time_patterns = {'medium': 'HH:mm:ss'}
        self.cal._date_patterns = {'medium': 'dd.MM.yyyy'}
        self.cal._datetime_pattern = '{1} {0}'
        
    def testInterfaceConformity(self):
        self.assert_(ILocaleCalendar.isImplementedBy(self.cal))

    def test_setMonth(self):
        self.cal.setMonth(2, 'February', 'Feb')
        self.assertEqual(self.cal._months,
                         {1: ('January', 'Jan'), 2: ('February', 'Feb')})

    def test_getMonth(self):
        self.assertEqual(self.cal.getMonth(1), ('January', 'Jan'))

    def test_getMonthNames(self):
        self.cal._months[2] = ('February', 'Feb')
        self.assertEqual(self.cal.getMonthNames(),
                         ['January', 'February'] + [None]*10)

    def test_getMonthIdFromName(self):
        self.assertEqual(self.cal.getMonthIdFromName('January'), 1)

    def test_getMonthAbbr(self):
        self.cal._months[2] = ('February', 'Feb')
        self.assertEqual(self.cal.getMonthAbbr(), ['Jan', 'Feb'] + [None]*10)

    def test_getMonthIdFromAbbr(self):
        self.assertEqual(self.cal.getMonthIdFromAbbr('Jan'), 1)

    def test_setWeekday(self):
        self.cal.setWeekday(2, 'Monday', 'Mo')
        self.assertEqual(self.cal._weekdays,
                         {1: ('Sunday', 'Su'), 2: ('Monday', 'Mo')})

    def test_getWeekday(self):
        self.assertEqual(self.cal.getWeekday(1), ('Sunday', 'Su'))

    def test_getWeekdayNames(self):
        self.cal._weekdays[2] = ('Monday', 'Mo')
        self.assertEqual(self.cal.getWeekdayNames(),
                         ['Sunday', 'Monday'] + [None]*5)

    def test_getWeekdayIdFromName(self):
        self.assertEqual(self.cal.getWeekdayIdFromName('Sunday'), 1)

    def test_getWeekdayAbbr(self):
        self.cal._weekdays[2] = ('Monday', 'Mo')
        self.assertEqual(self.cal.getWeekdayAbbr(), ['Su', 'Mo'] + [None]*5)

    def test_getWeekdayIdFromAbbr(self):
        self.assertEqual(self.cal.getWeekdayIdFromAbbr('Su'), 1)

    def test_setEra(self):
        self.cal.setEra(1, 'A.C.')
        self.assertEqual(self.cal._eras, {0: 'B.C.', 1: 'A.C.'})

    def test_getEra(self):
        self.assertEqual(self.cal.getEra(0), 'B.C.')

    def test_setAM(self):
        self.cal.setAM('vorm.')
        self.assertEqual(self.cal._am, 'vorm.')

    def test_getAM(self):
        self.assertEqual(self.cal.getAM(), 'AM')

    def test_setPM(self):
        self.cal.setPM('nachm.')
        self.assertEqual(self.cal._pm, 'nachm.')

    def test_getPM(self):
        self.assertEqual(self.cal.getPM(), 'PM')

    def test_setPatternCharacters(self):
        self.cal.setPatternCharacters('abc')
        self.assertEqual(self.cal._pattern_chars, 'abc')

    def test_getPatternCharacters(self):
        self.assertEqual(self.cal.getPatternCharacters(),
                         'GjMtkHmsSEDFwWahKzJe')

    def test_setTimePattern(self):
        self.cal.setTimePattern('long', 'HH:mm:ss z')
        self.assertEqual(self.cal._time_patterns,
                         {'medium': 'HH:mm:ss', 'long': 'HH:mm:ss z'})
        
    def test_getTimePattern(self):
        self.assertEqual(self.cal.getTimePattern('medium'), 'HH:mm:ss')

    def test_setDatePattern(self):
        self.cal.setDatePattern('long', 'd. MMMM yyyy')
        self.assertEqual(self.cal._date_patterns,
                         {'medium': 'dd.MM.yyyy', 'long': 'd. MMMM yyyy'})

    def test_getDatePattern(self):
        self.assertEqual(self.cal.getDatePattern('medium'), 'dd.MM.yyyy')

    def test_setDateTimePattern(self):
        self.cal.setDateTimePattern('{0} {1}')
        self.assertEqual(self.cal._datetime_pattern, '{0} {1}')

    def test_getDateTimePattern(self):
        self.assertEqual(self.cal.getDateTimePattern(), '{1} {0}')


class TestICULocaleNumberFormat(TestCase):

    def setUp(self):
        self.format = ICULocaleNumberFormat('decimal')
        self.format._patterns = {'decimal': '#,##0.###;-#,##0.###'}
        self.format._symbols = {'decimal': '.'}

    def testInterfaceConformity(self):
        self.assert_(ILocaleNumberFormat.isImplementedBy(self.format))

    def test_setPattern(self):
        self.format.setPattern('percent', '#,##0%')
        self.assertEqual(self.format._patterns,
                         {'decimal': '#,##0.###;-#,##0.###',
                          'percent': '#,##0%'})

    def test_getPattern(self):
        self.assertEqual(self.format.getPattern('decimal'),
                         '#,##0.###;-#,##0.###')

    def test_getAllPatternIds(self):
        self.format._patterns['percent'] = '#,##0%'
        ids = self.format.getAllPatternIds()
        ids.sort()
        self.assertEqual(ids, ['decimal', 'percent'])

    def test_setSymbol(self):
        self.format.setSymbol('percentSign', '%')
        self.assertEqual(self.format._symbols,
                         {'decimal': '.', 'percentSign': '%'})

    def test_getSymbol(self):
        self.assertEqual(self.format.getSymbol('decimal'), '.')

    def test_getAllSymbolIds(self):
        self.format._symbols['percentSign'] = '%'
        ids = self.format.getAllSymbolIds()
        ids.sort()
        self.assertEqual(ids, ['decimal', 'percentSign'])

    def test_getSymbolMap(self):
        self.assertEqual(self.format.getSymbolMap(), {'decimal': '.'})
        

class TestICULocaleCurrency(TestCase):

    def setUp(self):
        self.curr = ICULocaleCurrency('USD')
        self.curr._symbol = '$'
        self.curr._name = 'USD'
        self.curr._decimal = '.'
        self.curr._pattern = '$ #,##0.00;-$ #,##0.00'

    def testInterfaceConformity(self):
        self.assert_(ILocaleCurrency.isImplementedBy(self.curr))

    def test_setSymbol(self):
        self.curr.setSymbol(u'\u20ac')
        self.assertEqual(self.curr._symbol, u'\u20ac')

    def test_getSymbol(self):
        self.assertEqual(self.curr.getSymbol(), '$')
        
    def test_setName(self):
        self.curr.setName('EUR')
        self.assertEqual(self.curr._name, 'EUR')

    def test_getName(self):
        self.assertEqual(self.curr.getName(), 'USD')

    def test_setDecimal(self):
        self.curr.setDecimal(',')
        self.assertEqual(self.curr._decimal, ',')

    def test_getDecimal(self):
        self.assertEqual(self.curr.getDecimal(), '.')

    def test_setPattern(self):
        self.curr.setPattern('EUR #,##0.00;-EUR #,##0.00')
        self.assertEqual(self.curr._pattern, 'EUR #,##0.00;-EUR #,##0.00')

    def test_getPattern(self):
        self.assertEqual(self.curr.getPattern(), '$ #,##0.00;-$ #,##0.00')


class TestICUXMLLocaleFactory(TestCase):

    def setUp(self):
        org = os.curdir
        os.chdir(os.path.join(testdir(), 'xmllocales'))
        self.factory0 = ICUXMLLocaleFactory(
            os.path.join(testdir(), 'xmllocales', 'root.xml'))
        self.factory = ICUXMLLocaleFactory(
            os.path.join(testdir(), 'xmllocales', 'de.xml'))
        self.factory2 = ICUXMLLocaleFactory(
            os.path.join(testdir(), 'xmllocales', 'de_DE.xml'))
        self.factory3 = ICUXMLLocaleFactory(
            os.path.join(testdir(), 'xmllocales', 'de_DE_PREEURO.xml'))
        os.chdir(org)
        
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
        self.assertEqual(id.getLanguage(), 'de')
        self.assertEqual(id.getVariant(), None)
        self.assertEqual(id.getCountry(), None)
        self.assertEqual(id.getAllCorrespondences(), [(u'0007', u'Windows')])
        self.assertEqual(id.__repr__(), '<ICULocaleIdentity (de, None, None)>')

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
        self.assertEqual(zone[1].getCities(), [u'Berlin'])
        self.assertEqual(zone[1].getName('generic'),
                         (u'Mitteleurop\xe4ische Zeit', u'Europe/Berlin'))
        self.assertEqual(zone[2], True)

    def test_extractCalendars(self):
        cals = self.factory._extractCalendars()
        self.assertEqual(len(cals), 1)
        cal = cals[0]
        self.assertEqual(cal[0], u'gregorian')
        self.assertEqual(cal[0], cal[1].klass)
        self.assertEqual(cal[1].getMonth(1), (u'Januar', u'Jan'))
        self.assertEqual(cal[1].getWeekday(1), (u'Sonntag', u'So'))
        self.assertEqual(cal[2], True)

    def test_extractNumberFormats(self):
        formats = self.factory0._extractNumberFormats()
        self.assertEqual(len(formats), 1)
        format = formats[0]
        self.assertEqual(format[0], u'decimal')
        self.assertEqual(format[0], format[1].klass)
        self.assertEqual(format[1].getPattern('decimal'),
                         '#,##0.###;-#,##0.###')
        self.assertEqual(format[1].getPattern('percent'), '#,##0%')
        self.assertEqual(format[1].getPattern('scientific'), '#E0')
        self.assertEqual(format[1].getSymbol('percentSign'), u'%')
        self.assertEqual(format[1].getSymbol('nativeZeroDigit'), u'0')
        self.assertEqual(format[1].getSymbol('exponential'), u'E')
        self.assertEqual(format[1].getSymbol('perMille'), u'\u2030')
        self.assertEqual(format[2], True)

    def test_extractCurrencies(self):
        currs = self.factory3._extractCurrencies()
        self.assertEqual(len(currs), 1)
        curr = currs[0]
        self.assertEqual(curr[0], u'DEM')
        self.assertEqual(curr[0], curr[1].id)
        self.assertEqual(curr[1].getSymbol(), u'DM')
        self.assertEqual(curr[1].getName(), u'DEM')
        self.assertEqual(curr[1].getDecimal(), u',')
        self.assertEqual(curr[1].getPattern(), None)
        self.assertEqual(curr[2], True)
    

class TestILocale(TestCase):

    def _newLocale(self):
        raise NotImplemented

    def setUp(self):
        self.locale = self._newLocale()


class TestICULocale(TestILocale):
    
    def _newLocale(self):
        org = os.curdir
        os.chdir(os.path.join(testdir(), 'xmllocales'))
        path = os.path.join(testdir(), 'xmllocales', 'root.xml')
        localeFactory = ICUXMLLocaleFactory(path)
        os.chdir(org)
        return localeFactory()

    def testId(self):
        id = self.locale.id
        self.assertEqual(id.getLanguage(), None)
        self.assertEqual(id.getVariant(), None)
        self.assertEqual(id.getCountry(), None)
        self.assertEqual(id.getAllCorrespondences(), [(u'0000', u'Windows')])

    def test_getAllVersions(self):
        versions = self.locale.getAllVersions()
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions, self.locale._versions)
        self.assertEqual(versions[0].id, u'1.0')

    def test_getLatestVersion(self):
        self.assertEqual(self.locale.getLatestVersion().id, u'1.0')

    def test_getLanguageName(self):
        self.assertEqual(self.locale.getLanguageName('de'), 'German')
        self.assertEqual(self.locale.getLanguageName('ab'), 'Abkhazian')
        self.assertEqual(self.locale.getLanguageName('zh'), 'Chinese')

    def test_getAllLanguageIds(self):
        ids = self.locale.getAllLanguageIds()
        self.assertEqual(len(ids), 436)
        self.assert_('de' in ids)
        self.assert_('ab' in ids)
        self.assert_('zh' in ids)
        self.assert_('xx' not in ids)

    def test_getCountryName(self):
        self.assertEqual(self.locale.getCountryName('DE'), 'Germany')
        self.assertEqual(self.locale.getCountryName('AE'),
                         'United Arab Emirates')
        self.assertEqual(self.locale.getCountryName('ZW'), 'Zimbabwe')

    def test_getAllCountryIds(self):
        ids = self.locale.getAllCountryIds()
        self.assertEqual(len(ids), 240)
        self.assert_('DE' in ids)
        self.assert_('AE' in ids)
        self.assert_('ZW' in ids)
        self.assert_('XX' not in ids)

    def test_getTimeZone(self):
        zone = self.locale.getTimeZone(u'EST')
        self.assertEqual(zone.id, u'EST')
        self.assertEqual(zone.getCities(), [u'New York'])
        self.assertEqual(zone.getName('generic'),
                         (u'Eastern Standard Time',
                          u'EST'))

    def test_getDefaultTimeZone(self):
        zone = self.locale.getDefaultTimeZone()
        self.assertEqual(zone.id, u'PST')

    def test_getTimeZoneIds(self):
        ids = self.locale.getTimeZoneIds()
        self.assertEqual(len(ids), 9)
        self.assert_(u'EST' in ids)

    def test_getCalendar(self):
        cal = self.locale.getCalendar(u'gregorian')
        self.assertEqual(cal.klass, u'gregorian')
        self.assertEqual(cal.getMonth(1), (u'January', u'Jan'))
        self.assertEqual(cal.getWeekday(1), (u'Sunday', u'Sun'))
        self.assertEqual(cal.getDatePattern('full'), 'EEEE, MMMM d, yyyy')
        
    def test_getDefaultCalendar(self):
        cal = self.locale.getDefaultCalendar()
        self.assertEqual(cal.klass, u'gregorian')

    def test_getCalendarClasses(self):
        ids = self.locale.getCalendarClasses()
        self.assertEqual(ids, [u'gregorian'])

    def test_getNumberFormat(self):
        format = self.locale.getNumberFormat(u'decimal')
        self.assertEqual(format.klass, u'decimal')
        self.assertEqual(format.getPattern('decimal'), u'#,##0.###;-#,##0.###')
        self.assertEqual(format.getSymbol('exponential'), u'E')
        
    def test_getDefaultNumberFormat(self):
        format = self.locale.getDefaultNumberFormat()
        self.assertEqual(format.klass, u'decimal')

    def test_getNumberFormatClasses(self):
        klasses = self.locale.getNumberFormatClasses()
        self.assertEqual(klasses, [u'decimal'])

    def test_getCurrency(self):
        curr = self.locale.getCurrency(u'XXX')
        self.assertEqual(curr.id, u'XXX')
        self.assertEqual(curr.getName(), u'XXX')
        self.assertEqual(curr.getSymbol(), u'\xa4')
        self.assertEqual(curr.getDecimal(), u'.')
        
    def test_getDefaultCurrency(self):
        curr = self.locale.getDefaultCurrency()
        self.assertEqual(curr.id, u'XXX')

    def test_getCurrencyIds(self):
        ids = self.locale.getCurrencyIds()
        self.assertEqual(ids, [u'XXX'])


class TestICULocaleAndProvider(TestCase):
    
    def setUp(self):
        orig = locales._locale_dir
        locales._locale_dir = os.path.join(testdir(), 'xmllocales')
        locales.loadLocale(None, None, None)
        locales.loadLocale('de', None, None)
        locales.loadLocale('de', 'DE', None)
        locales.loadLocale('de', 'DE', 'PREEURO')
        self.locale = locales.getLocale('de', 'DE', 'PREEURO')
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
        self.assertEqual(locale.id.getLanguage(), 'de')
        self.assertEqual(locale.id.getCountry(), 'AT')
        self.assertEqual(locale.id.getVariant(), None)


def test_suite():
    return TestSuite((
        makeSuite(TestLocaleProvider),
        makeSuite(TestICULocaleIdentity),
        makeSuite(TestICULocaleVersion),
        makeSuite(TestICULocaleTimeZone),
        makeSuite(TestICULocaleCalendar),
        makeSuite(TestICULocaleNumberFormat),
        makeSuite(TestICULocaleCurrency),
        makeSuite(TestICUXMLLocaleFactory),
        makeSuite(TestICULocale),
        makeSuite(TestICULocaleAndProvider),
        makeSuite(TestGlobalLocaleProvider),
        ))
