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
"""Locale and LocaleProvider Implementation.

$Id: locales.py,v 1.17 2003/11/05 03:08:14 jeremy Exp $
"""
import os
import datetime
from xml.dom.minidom import parse as parseXML
from zope.interface import implements

from time import strptime

from zope.i18n.interfaces import ILocaleProvider, ILocale
from zope.i18n.interfaces import ILocaleVersion, ILocaleIdentity
from zope.i18n.interfaces import ILocaleTimeZone, ILocaleCalendar
from zope.i18n.interfaces import ILocaleNumberFormat, ILocaleCurrency

from zope.i18n.format import NumberFormat, DateTimeFormat

# Setup the locale directory
from zope import i18n
LOCALEDIR = os.path.join(os.path.dirname(i18n.__file__), "locales")

# Define some constants that can be used

JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7

BC = 0
AD = 1


class NoGeneralLocaleError(Exception):
    """This error is raised when no more general locale is found in the
    provider."""

class LoadLocaleError(Exception):
    """This error is raised if a locale cannot be loaded."""

class LocaleProvider:
    __doc__ = ILocaleProvider.__doc__

    implements(ILocaleProvider)


    def __init__(self, locale_dir):
        self._locales = {}
        self._locale_dir = locale_dir

    def loadLocale(self, language=None, country=None, variant=None):
        "See ZopeProducts.LocaleProvider.interfaces.ILocaleProvider"
        # Creating the filename
        if language == None and country == None and variant == None:
            filename = 'root.xml'
        else:
            filename = language
            if country is not None:
                filename += '_'+country
            if variant is not None:
                if '_' not in filename:
                    filename += '_'
                filename += '_'+variant
            filename += '.xml'

        # Making sure we have this locale
        path = os.path.join(self._locale_dir, filename)
        if not os.path.exists(path):
            raise LoadLocaleError, \
                  'The desired locale is not available.\nPath: %s' %path

        # Let's get it!
        locale = XMLLocaleFactory(path)()
        self._locales[(language, country, variant)] = locale

    def getLocale(self, language=None, country=None, variant=None):
        "See ZopeProducts.LocaleProvider.interfaces.ILocaleProvider"
        # We want to be liberal in what we accept, but the standard is lower
        # case language codes, upper case country codes, and upper case
        # variants, so coerce case here.
        if language:
            language = language.lower()
        if country:
            country = country.upper()
        if variant:
            variant = variant.upper()
        if not self._locales.has_key((language, country, variant)):
            self.loadLocale(language, country, variant)
        return self._locales[(language, country, variant)]

# Global LocaleProvider. We really just need this single one.
locales = LocaleProvider(LOCALEDIR)


class LocaleIdentity:
    __doc__ = ILocaleIdentity.__doc__

    implements(ILocaleIdentity)

    def __init__(self, language=None, country=None, variant=None):
        """Initialize object."""
        self.language = language
        self.country = country
        self.variant = variant
        self.correspondsTos = []

    def __repr__(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return "<LocaleIdentity (%s, %s, %s)>" %(
            self.language, self.country, self.variant)


class LocaleVersion:
    __doc__ = ILocaleVersion.__doc__

    implements(ILocaleVersion)

    # See zope.i18n.interfaces.ILocaleVersion
    id = None
    # See zope.i18n.interfaces.ILocaleVersion
    date = None
    # See zope.i18n.interfaces.ILocaleVersion
    comment = None

    def __init__(self, id, date, comment):
        """Initialize object."""
        self.id = id
        assert(isinstance(date, datetime.datetime))
        self.date = date
        self.comment = comment

    def __cmp__(self, other):
        "See zope.i18n.interfaces.ILocaleVersion"
        return cmp(self.date, other.date)


class LocaleTimeZone:
    __doc__ = ILocaleTimeZone.__doc__

    implements(ILocaleTimeZone)

    def __init__(self, id):
        """Initialize the object."""
        self.id = id
        self.cities = []
        self.names = {}


class LocaleCalendar:
    __doc__ = ILocaleCalendar.__doc__

    implements(ILocaleCalendar)

    def __init__(self, klass):
        """Initialize the object."""
        self.klass = klass
        self.months = {}
        self.weekdays = {}
        self.eras = {0: '', 1: ''}
        self.am = u''
        self.pm = u''
        self.patternCharacters = u''
        self.timePatterns = {}
        self.datePatterns = {}
        self.datetimePattern = u''

    def update(self, other):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self.months.update(other.months)
        self.weekdays.update(other.weekdays)
        self.eras.update(other.eras)
        if other.am != u'':
            self.am = other.am
        if other.pm != u'':
            self.pm = other.pm
        if other.patternCharacters != u'':
            self.patternCharacters = other.patternCharacters
        self.timePatterns.update(other.timePatterns)
        self.datePatterns.update(other.datePatterns)
        if other.datetimePattern != u'':
            self.datetimePattern = other.datetimePattern

        return self.months[id]

    def getMonthNames(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        names = []
        for id in range(1, 13):
            names.append(self.months.get(id, (None, None))[0])
        return names

    def getMonthIdFromName(self, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self.months.items():
            if item[1][0] == name:
                return item[0]

    def getMonthAbbr(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        abbrs = []
        for id in range(1, 13):
            abbrs.append(self.months.get(id, (None, None))[1])
        return abbrs

    def getMonthIdFromAbbr(self, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self.months.items():
            if item[1][1] == abbr:
                return item[0]

    def getWeekdayNames(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        names = []
        for id in range(1, 8):
            names.append(self.weekdays.get(id, (None, None))[0])
        return names

    def getWeekdayIdFromName(self, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self.weekdays.items():
            if item[1][0] == name:
                return item[0]

    def getWeekdayAbbr(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        abbrs = []
        for id in range(1, 8):
            abbrs.append(self.weekdays.get(id, (None, None))[1])
        return abbrs

    def getWeekdayIdFromAbbr(self, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self.weekdays.items():
            if item[1][1] == abbr:
                return item[0]


class LocaleNumberFormat:
    __doc__ = ILocaleNumberFormat.__doc__

    implements(ILocaleNumberFormat)

    def __init__(self, klass):
        """Initialize object."""
        self.klass = klass
        self.patterns = {}
        self.symbols = {}


class LocaleCurrency:
    __doc__ = ILocaleCurrency.__doc__

    implements(ILocaleCurrency)

    def __init__(self, id):
        """Initialize object."""
        self.id = id
        self.symbol = None
        self.name = None
        self.decimal = None
        self.pattern = None


class Locale:
    __doc__ = ILocale.__doc__

    implements(ILocale)

    def __init__(self, id):
        self.id = id
        self.versions = []
        self.languages = {}
        self.countries = {}
        self.timezones = {}
        self.calendars = {}
        self.numberFormats = {}
        self.currencies = {}
        self._default_tzid = None
        self._default_cal_class = None
        self._default_numformat_class = None
        self._default_currency_id = None

    def getLatestVersion(self):
        """Return latest version (by date)."""
        if len(self.versions) == 0: return None
        def greater(v1, v2):
            """Return version with greater datetime."""
            if v1 > v2: return v1
            else: return v2
        return reduce(greater, self.versions)

    def getDefaultTimeZone(self):
        """Return the default time zone."""
        if not self._default_tzid:
            return None
        return self.timezones[self._default_tzid]

    def getDefaultCalendar(self):
        """Return the default calendar."""
        if not self._default_cal_class:
            return None
        return self.calendars[self._default_cal_class]

    def getDefaultNumberFormat(self):
        """Return the default number format."""
        if not self._default_numformat_class:
            return None
        return self.numberFormats[self._default_numformat_class]

    def getDefaultCurrency(self):
        """Return the currency format."""
        if not self._default_currency_id:
            return None
        return self.currencies[self._default_currency_id]

    def _getNextLocale(self):
        """This is the really interesting method that looks up the next (more
        general) Locale object. This is used in case thi slocale object does
        not have the required information.

        This method works closely with with LocaleProvider.
        """
        language = self.id.language
        country = self.id.country
        variant = self.id.variant
        if variant is not None:
            return locales.getLocale(language, country, None)
        elif country is not None:
            return locales.getLocale(language, None, None)
        elif language is not None:
            return locales.getLocale(None, None, None)
        else:
            # Well, this is bad; we are already at the root locale
            raise NoGeneralLocaleError, 'Cannot find more general locale.'

    def _createFullCalendar(self):
        '''For the date/time formatters we need a full-blown calendar object
        that has no missing information. This methos will build this
        object.'''
        calendar = LocaleCalendar('gregorian')
        for id in ((None, None, None),
                   (self.id.language, None, None),
                   (self.id.language, self.id.country, None),
                   (self.id.language, self.id.country,
                    self.id.variant)):
            try:
                calendar.update(locales.getLocale(*id).calendars['gregorian'])
            except KeyError:
                pass # Locale has no calendar information
        return calendar

    def getDisplayLanguage(self, id):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            return self.languages[id]
        except KeyError:
            try:
                return self._getNextLocale().getDisplayLanguage(id)
            except NoGeneralLocaleError:
                raise KeyError, "Language '%s' not found." %id

    def getDisplayCountry(self, id):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            return self.countries[id]
        except KeyError:
            try:
                return self._getNextLocale().getDisplayCountry(id)
            except NoGeneralLocaleError:
                raise KeyError, "Country '%s' not found." %id

    def getTimeFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().timePatterns[name]
        except (AttributeError, KeyError):
            return self._getNextLocale().getTimeFormatter(name)
        if not pattern:
            return self._getNextLocale().getTimeFormatter(name)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getDateFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().datePatterns[name]
        except (AttributeError, KeyError):
            return self._getNextLocale().getDateFormatter(name)
        if not pattern:
            return self._getNextLocale().getDateFormatter(name)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getDateTimeFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().datetimePattern
        except (AttributeError, KeyError):
            return self._getNextLocale().getDateTimeFormatter(name)
        if not pattern:
            return self._getNextLocale().getDateTimeFormatter(name)
        date_pat = self.getDateFormatter(name).getPattern()
        time_pat = self.getTimeFormatter(name).getPattern()
        pattern = pattern.replace('{1}', date_pat)
        pattern = pattern.replace('{0}', time_pat)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getNumberFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultNumberFormat().patterns[name]
        except (AttributeError, KeyError):
            return self._getNextLocale().getNumberFormatter(name)
        if not pattern:
            return self._getNextLocale().getNumberFormatter(name)
        symbols = {}
        for id in ((None, None, None),
                   (self.id.language, None, None),
                   (self.id.language, self.id.country, None),
                   (self.id.language, self.id.country,
                    self.id.variant)):
            try:
                format = locales.getLocale(*id).getDefaultNumberFormat()
                symbols.update(format.symbols)
            except (AttributeError, KeyError):
                pass # Locale has no number format information

        return NumberFormat(pattern, symbols)


    def getCurrencyFormatter(self, name=None):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        if name is not None:
            try:
                currency = self.currencies[name]
            except (AttributeError, KeyError):
                currency = None
        else:
            currency = self.getDefaultCurrency()

        if currency is None:
            return self._getNextLocale().getCurrencyFormatter(name)

        symbols = {}
        for id in ((None, None, None),
                   (self.id.language, None, None),
                   (self.id.language, self.id.country, None),
                   (self.id.language, self.id.country,
                    self.id.variant)):
            try:
                format = locales.getLocale(*id).getDefaultNumberFormat()
                symbols.update(format.symbols)
            except (AttributeError, KeyError):
                pass # Locale has no number format information
        if currency.decimal:
            symbols['decimal'] = currency.decimal

        return NumberFormat(currency.pattern, symbols)


class XMLLocaleFactory:
    """This class creates a Locale object from an ICU XML file."""

    def __init__(self, path):
        """Initialize factory."""
        self._path = path
        self._data = parseXML(path).documentElement

    def _getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def _extractIdentity(self):
        """Extract the Locale's identity object based on info from the DOM
        tree."""
        args = {}
        # Define the language, if the file is not called 'root', in which
        # case the language remains to be 'None'
        if os.path.split(self._path)[1][:4] != 'root':
            args['language'] = os.path.split(self._path)[1][:2]
        identity = self._data.getElementsByTagName('identity')[0]
        nodes = identity.getElementsByTagName('country')
        if nodes != []:
            args['country'] = nodes[0].getAttribute('id')
        nodes = identity.getElementsByTagName('variant')
        if nodes != []:
            args['variant'] = nodes[0].getAttribute('id')
        id = LocaleIdentity(**args)
        nodes = identity.getElementsByTagName('correspondsTo')
        for node in nodes:
            vendor = node.getAttribute('vendor')
            id.correspondsTos.append((vendor, self._getText(node.childNodes)))
        return id


    def _extractVersions(self):
        """Extract all versioning information from the DOM tree."""
        versions = []
        versioning = self._data.getElementsByTagName('versioning')[0]
        for version in versioning.getElementsByTagName('version'):
            id = version.getAttribute('number')
            date = version.getAttribute('date')
            date = strptime(date, '%a %b %d %H:%M:%S %Y')
            date = datetime.datetime(*date[:6])
            comment = self._getText(version.childNodes)
            versions.append(LocaleVersion(id, date, comment))
        return versions


    def _extractLanguages(self):
        """Extract all languages from the DOM tree."""
        try:
            names = self._data.getElementsByTagName('displayNames')[0]
            langs = names.getElementsByTagName('languages')[0]
        except IndexError:
            return {}
        languages = {}
        nodes = langs.getElementsByTagName('language')
        for node in nodes:
            languages[node.getAttribute('id')] = self._getText(node.childNodes)
        return languages


    def _extractCountries(self):
        """Extract all countries from the DOM tree."""
        try:
            names = self._data.getElementsByTagName('displayNames')[0]
            countries = names.getElementsByTagName('countries')[0]
        except IndexError:
            return {}
        nodes = countries.getElementsByTagName('country')
        countries = {}
        for node in nodes:
            countries[node.getAttribute('id')] = self._getText(node.childNodes)
        return countries


    def _extractTimeZones(self):
        """Extract all timezone information for the locale from the DOM
        tree."""
        try:
            names = self._data.getElementsByTagName('timeZoneNames')[0]
        except IndexError:
            return []
        nodes = names.getElementsByTagName('zone')
        zones = []
        for node in nodes:
            id = node.getAttribute('id')
            zone = LocaleTimeZone(id)
            default = node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False
            long = node.getElementsByTagName('long')[0]
            short = node.getElementsByTagName('short')[0]
            for type in ('generic', 'standard', 'daylight'):
                try:
                    long_desc = self._getText(
                        long.getElementsByTagName(type)[0].childNodes)
                except IndexError:
                    long_desc = None # no long description
                try:
                    short_desc = self._getText(
                        short.getElementsByTagName(type)[0].childNodes)
                except IndexError:
                    short_desc = None # no short description
                if long_desc is not None or short_desc is not None:
                    zone.names[type] = (long_desc, short_desc)
            for city in node.getElementsByTagName('city'):
                zone.cities.append(self._getText(city.childNodes))
            zones.append((id, zone, default))

        return zones


    def _extractMonths(self, cal_node, calendar):
        try:
            names_node = cal_node.getElementsByTagName('monthNames')[0]
        except IndexError:
            return
        names = {}
        for name_node in names_node.getElementsByTagName('month'):
            id = int(name_node.getAttribute('id'))
            names[id] = self._getText(name_node.childNodes)
        abbrs_node = cal_node.getElementsByTagName('monthAbbr')[0]
        abbr = {}
        for abbr_node in abbrs_node.getElementsByTagName('month'):
            id = int(abbr_node.getAttribute('id'))
            abbr[id] = self._getText(abbr_node.childNodes)
        for id in range(1, 13):
            calendar.months[id] = (names.get(id, None), abbr.get(id, None))


    def _extractWeekdays(self, cal_node, calendar):
        names_node = cal_node.getElementsByTagName('dayNames')
        names = {}
        if names_node:
            names_node = names_node[0]
            for name_node in names_node.getElementsByTagName('day'):
                id = int(name_node.getAttribute('id'))
                names[id] = self._getText(name_node.childNodes)
        abbrs_node = cal_node.getElementsByTagName('dayAbbr')
        abbr = {}
        if abbrs_node:
            abbrs_node = abbrs_node[0]
            for abbr_node in abbrs_node.getElementsByTagName('day'):
                id = int(abbr_node.getAttribute('id'))
                abbr[id] = self._getText(abbr_node.childNodes)
        for id in range(1, 8):
            # For some reason the ICU XML Files leave a space behind the
            # weekday names, so that we have to strip them down.
            name = names.get(id, None)
            if isinstance(name, unicode):
                name = name.strip()
            abb = abbr.get(id, None)
            if isinstance(abb, unicode):
                abb = abb.strip()
            calendar.weekdays[id] = (name, abb)


    def _extractEras(self, cal_node, calendar):
        eras_node = cal_node.getElementsByTagName('eras')
        if eras_node:
            eras_node = eras_node[0]
            for era_node in eras_node.getElementsByTagName('era'):
                id = int(era_node.getAttribute('id'))
                calendar.eras[id] = self._getText(era_node.childNodes)


    def _extractCalendarPatterns(self, cal_node, calendar):
        try:
            pat_node = cal_node.getElementsByTagName('patterns')[0]
        except IndexError:
            return
        chars_node = pat_node.getElementsByTagName('chars')
        if chars_node:
            chars_node = chars_node[0]
            calendar.patternCharacters = self._getText(chars_node.childNodes)
        try:
            time_node = cal_node.getElementsByTagName('time')[0]
            date_node = cal_node.getElementsByTagName('date')[0]
        except IndexError:
            return
        for type in ('full', 'long', 'medium', 'short'):
            node = time_node.getElementsByTagName(type)[0]
            calendar.timePatterns[type] = self._getText(node.childNodes)
            node = date_node.getElementsByTagName(type)[0]
            calendar.datePatterns[type] = self._getText(node.childNodes)
        datetime_node = cal_node.getElementsByTagName('dateTime')[0]
        calendar.datetimePattern = self._getText(datetime_node.childNodes)

    def _extractCalendars(self):
        """Extract all calendars and their specific information from the
        Locale's DOM tree."""
        calendars = []
        try:
            cals_node = self._data.getElementsByTagName('calendars')[0]
        except IndexError:
            # no calendar node
            return []
        for cal_node in cals_node.getElementsByTagName('calendar'):
            klass = cal_node.getAttribute('class')
            calendar = LocaleCalendar(klass)
            default = cal_node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False
            nodes = cal_node.getElementsByTagName('am')
            if nodes:
                calendar.am = self._getText(nodes[0].childNodes)
            nodes = cal_node.getElementsByTagName('pm')
            if nodes:
                calendar.pm = self._getText(nodes[0].childNodes)
            self._extractMonths(cal_node, calendar)
            self._extractWeekdays(cal_node, calendar)
            self._extractEras(cal_node, calendar)
            self._extractCalendarPatterns(cal_node, calendar)
            calendars.append((klass, calendar, default))
        return calendars


    def _extractNumberFormats(self):
        """Extract all number format information from the Locale's DOM
        tree."""
        formats = []
        for format_node in self._data.getElementsByTagName('numberFormat'):
            klass = format_node.getAttribute('class')
            format = LocaleNumberFormat(klass)
            default = format_node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False

            pattern_nodes = format_node.getElementsByTagName('patterns')
            if len(pattern_nodes) == 1:
                node = pattern_nodes[0]
                for field in ('decimal', 'percent', 'scientific'):
                    field_node = node.getElementsByTagName(field)[0]
                    format.patterns[field] = self._getText(
                        field_node.childNodes)

            symbols_nodes = format_node.getElementsByTagName('symbols')
            if len(symbols_nodes) == 1:
                node = symbols_nodes[0]
                for field in ('decimal', 'group', 'list', 'percentSign',
                              'nativeZeroDigit', 'patternDigit', 'plusSign',
                              'minusSign', 'exponential', 'perMille',
                              'infinity', 'nan'):
                    try:
                        field_node = node.getElementsByTagName(field)[0]
                        format.symbols[field] = self._getText(
                            field_node.childNodes)
                    except IndexError:
                        pass # node does not exist

            formats.append((klass, format, default))

        return formats


    def _extractCurrencies(self):
        """Extract all currency definitions and their information from the
        Locale's DOM tree."""
        currencies = []
        try:
            currs_node = self._data.getElementsByTagName('currencies')[0]
        except IndexError:
            # no currencies node
            return []
        for curr_node in currs_node.getElementsByTagName('currency'):
            id = curr_node.getAttribute('id')
            currency = LocaleCurrency(id)
            default = curr_node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False
            node = curr_node.getElementsByTagName('symbol')[0]
            currency.symbol = self._getText(node.childNodes)
            node = curr_node.getElementsByTagName('name')[0]
            currency.name = self._getText(node.childNodes)
            try:
                node = curr_node.getElementsByTagName('decimal')[0]
                currency.decimal = self._getText(node.childNodes)
            except IndexError:
                pass # No decimal node
            try:
                node = curr_node.getElementsByTagName('pattern')[0]
                currency.pattern = self._getText(node.childNodes)
            except IndexError:
                pass # No pattern node

            currencies.append((id, currency, default))

        return currencies


    def __call__(self):
        """Create the Locale."""
        locale = Locale(self._extractIdentity())
        locale.versions = self._extractVersions()
        locale.languages = self._extractLanguages()
        locale.countries = self._extractCountries()
        # Set TimeZones
        for id, tz, default in self._extractTimeZones():
            locale.timezones[id] = tz
            if default:
                locale._default_tzid = id

        # Set Calendars
        for klass, calendar, default in self._extractCalendars():
            locale.calendars[klass] = calendar
            if default:
                locale._default_cal_class = klass

        # Set Number Formats
        for klass, format, default in self._extractNumberFormats():
            locale.numberFormats[klass] = format
            if default:
                locale._default_numformat_class = klass

        # Set Currencies
        for id, currency, default in self._extractCurrencies():
            locale.currencies[id] = currency
            if default:
                locale._default_currency_id = id

        return locale

