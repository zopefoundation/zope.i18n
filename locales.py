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

$Id: locales.py,v 1.9 2003/03/25 14:30:06 bwarsaw Exp $
"""
import os
import datetime
from xml.dom.minidom import parse as parseXML

# time.strptime() isn't available on all platforms before Python 2.3.  When
# it isn't available, use the implementation from 2.3's _strptime.py, checked
# into this source tree for convenience.  This workaround can be removed
# when Python 2.3 (or later) becomes required.
try:
    from time import strptime
except ImportError:
    from _strptime import strptime

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

    __implements__ =  ILocaleProvider


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
        locale = ICUXMLLocaleFactory(path)()
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


class ICULocaleIdentity:
    __doc__ = ILocaleIdentity.__doc__

    __implements__ =  ILocaleIdentity

    def __init__(self, language=None, country=None, variant=None):
        """Initialize object."""
        self.__language = language
        self.__country = country
        self.__variant = variant
        self._correspondsTos = []

    def getLanguage(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return self.__language

    def getCountry(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return self.__country

    def getVariant(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return self.__variant

    def setCorrespondence(self, vendor, text):
        "See zope.i18n.interfaces.ILocaleIdentity"
        self._correspondsTos.append((vendor, text))

    def getAllCorrespondences(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return self._correspondsTos

    def __repr__(self):
        "See zope.i18n.interfaces.ILocaleIdentity"
        return "<ICULocaleIdentity (%s, %s, %s)>" %(
            self.__language, self.__country, self.__variant)


class ICULocaleVersion:
    __doc__ = ILocaleVersion.__doc__

    __implements__ = ILocaleVersion

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


class ICULocaleTimeZone:
    __doc__ = ILocaleTimeZone.__doc__

    __implements__ =  ILocaleTimeZone

    def __init__(self, id):
        """Initialize the object."""
        self.id = id
        self._cities = []
        self._names = {} # Possible ids: generic, standard, daylight

    def addCity(self, city):
        "See zope.i18n.interfaces.ILocaleTimeZone"
        self._cities.append(city)

    def getCities(self):
        "See zope.i18n.interfaces.ILocaleTimeZone"
        return self._cities

    def setName(self, type, long, short):
        "See zope.i18n.interfaces.ILocaleTimeZone"
        self._names[type] = (long, short)

    def getName(self, type):
        "See zope.i18n.interfaces.ILocaleTimeZone"
        return self._names[type]


class ICULocaleCalendar:
    __doc__ = ILocaleCalendar.__doc__

    __implements__ =  ILocaleCalendar

    def __init__(self, klass):
        """Initialize the object."""
        self.klass = klass
        self._months = {}
        self._weekdays = {}
        self._eras = {}
        self._am = u''
        self._pm = u''
        self._pattern_chars = ''
        self._time_patterns = {}
        self._date_patterns = {}
        self._datetime_pattern = u''

    def update(self, other):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._months.update(other._months)
        self._weekdays.update(other._weekdays)
        self._eras.update(other._eras)
        if other._am != u'':
            self._am = other._am
        if other._pm != u'':
            self._pm = other._pm
        if other._pattern_chars != u'':
            self._pattern_chars = other._pattern_chars
        self._time_patterns.update(other._time_patterns)
        self._date_patterns.update(other._date_patterns)
        if other._datetime_pattern != u'':
            self._datetime_pattern = other._datetime_pattern

    def setMonth(self, id, name, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        assert isinstance(id, int)
        self._months[id] = (name, abbr)

    def getMonth(self, id):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._months[id]

    def getMonthNames(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        names = []
        for id in range(1, 13):
            names.append(self._months.get(id, (None, None))[0])
        return names

    def getMonthIdFromName(self, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self._months.items():
            if item[1][0] == name:
                return item[0]

    def getMonthAbbr(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        abbrs = []
        for id in range(1, 13):
            abbrs.append(self._months.get(id, (None, None))[1])
        return abbrs

    def getMonthIdFromAbbr(self, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self._months.items():
            if item[1][1] == abbr:
                return item[0]

    def setWeekday(self, id, name, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._weekdays[id] = (name, abbr)

    def getWeekday(self, id):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._weekdays[id]

    def getWeekdayNames(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        names = []
        for id in range(1, 8):
            names.append(self._weekdays.get(id, (None, None))[0])
        return names

    def getWeekdayIdFromName(self, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self._weekdays.items():
            if item[1][0] == name:
                return item[0]

    def getWeekdayAbbr(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        abbrs = []
        for id in range(1, 8):
            abbrs.append(self._weekdays.get(id, (None, None))[1])
        return abbrs

    def getWeekdayIdFromAbbr(self, abbr):
        "See zope.i18n.interfaces.ILocaleCalendar"
        for item in self._weekdays.items():
            if item[1][1] == abbr:
                return item[0]

    def setEra(self, id, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._eras[id] = name

    def getEra(self, id):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._eras[id]

    def setAM(self, text):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._am = text

    def getAM(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._am

    def setPM(self, text):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._pm = text

    def getPM(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._pm

    def setPatternCharacters(self, chars):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._pattern_chars = chars

    def getPatternCharacters(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._pattern_chars

    def setTimePattern(self, type, pattern):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._time_patterns[type] = pattern

    def getTimePattern(self, type):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._time_patterns[type]

    def setDatePattern(self, name, pattern):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._date_patterns[name] = pattern

    def getDatePattern(self, name):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._date_patterns[name]

    def setDateTimePattern(self, pattern):
        "See zope.i18n.interfaces.ILocaleCalendar"
        self._datetime_pattern = pattern

    def getDateTimePattern(self):
        "See zope.i18n.interfaces.ILocaleCalendar"
        return self._datetime_pattern


class ICULocaleNumberFormat:
    __doc__ = ILocaleNumberFormat.__doc__

    __implements__ = ILocaleNumberFormat

    def __init__(self, klass):
        """Initialize object."""
        self.klass = klass
        self._patterns = {}
        self._symbols = {}

    def setPattern(self, name, pattern):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        self._patterns[name] = pattern

    def getPattern(self, name):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        return self._patterns[name]

    def getAllPatternIds(self):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        return self._patterns.keys()

    def setSymbol(self, name, symbol):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        self._symbols[name] = symbol

    def getSymbol(self, name):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        return self._symbols[name]

    def getAllSymbolIds(self):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        return self._symbols.keys()

    def getSymbolMap(self):
        "See zope.i18n.interfaces.ILocaleNumberFormat"
        return self._symbols


class ICULocaleCurrency:
    __doc__ = ILocaleCurrency.__doc__

    __implements__ = ILocaleCurrency

    def __init__(self, id):
        """Initialize object."""
        self.id = id
        self._symbol = None
        self._name = None
        self._decimal = None
        self._pattern = None

    def setSymbol(self, symbol):
        "See zope.i18n.interfaces.ILocaleCurrency"
        self._symbol = symbol

    def getSymbol(self):
        "See zope.i18n.interfaces.ILocaleCurrency"
        return self._symbol

    def setName(self, name):
        "See zope.i18n.interfaces.ILocaleCurrency"
        self._name = name

    def getName(self):
        "See zope.i18n.interfaces.ILocaleCurrency"
        return self._name

    def setDecimal(self, decimal):
        "See zope.i18n.interfaces.ILocaleCurrency"
        self._decimal = decimal

    def getDecimal(self):
        "See zope.i18n.interfaces.ILocaleCurrency"
        return self._decimal

    def setPattern(self, pattern):
        "See zope.i18n.interfaces.ILocaleCurrency"
        self._pattern = pattern

    def getPattern(self):
        "See zope.i18n.interfaces.ILocaleCurrency"
        return self._pattern


class ICULocale:
    __doc__ = ILocale.__doc__

    __implements__ = ILocale

    def __init__(self, id):
        self.id = id
        self._versions = []
        self._languages = {}
        self._countries = {}
        self._timezones = {}
        self._calendars = {}
        self._number_formats = {}
        self._currencies = {}
        self._default_tzid = None
        self._default_cal_class = None
        self._default_numformat_class = None
        self._default_currency_id = None

    # ICU-specific methods

    def setVersion(self, version):
        """Add a particular version."""
        self._versions.append(version)

    def getAllVersions(self):
        """Return a list of versions of the form (id, date, comment)."""
        return self._versions

    def getLatestVersion(self):
        """Return latest version (by date)."""
        if len(self._versions) == 0: return None
        def greater(v1, v2):
            """Return version with greater datetime."""
            if v1 > v2: return v1
            else: return v2
        return reduce(greater, self._versions)

    def setIdentity(self, id):
        """Define the unique identification object for this locale."""

    def setLanguageName(self, id, name):
        """Add a language in the locale's native language defined by its
        two-letter id."""
        self._languages[id] = name

    def updateLanguageNames(self, dict):
        """Add a dictionary of languages.

        The dict should map a two-letter id to the language in the locale's
        native language.
        """
        self._languages.update(dict)

    def getLanguageName(self, id):
        """Get the localized language name for the given id."""
        return self._languages[id]

    def getAllLanguageIds(self):
        """Return all available language ids."""
        return self._languages.keys()

    def setCountryName(self, id, name):
        """Add a country in the locale's native language defined by its
        two-letter id."""
        self._countries[id] = name

    def updateCountryNames(self, dict):
        """Add a dictionary of countries.

        The dict should map the country's two-letter id to the country's
        name in its native language.
        """
        self._countries.update(dict)


    def getCountryName(self, id):
        """Get the localized country name for the given id."""
        return self._countries[id]

    def getAllCountryIds(self):
        """Return all available country ids."""
        return self._countries.keys()

    def setTimeZone(self, id, timezone, default=False):
        """Add a new timezone for this locale. Note that all defined
        timezones are timezones the language of this locale is spoken."""
        self._timezones[id] = timezone
        if default:
            self._default_tzid = id

    def getTimeZone(self, id):
        """Get timezone by id."""
        return self._timezones[id]

    def getDefaultTimeZone(self):
        """Return the default time zone."""
        if not self._default_tzid:
            return None
        return self._timezones[self._default_tzid]

    def getTimeZoneIds(self):
        """Return all defined timezone ids."""
        return self._timezones.keys()

    def setCalendar(self, klass, calendar, default=False):
        """Add a new calendar for this locale."""
        self._calendars[klass] = calendar
        if default:
            self._default_cal_class = klass

    def getCalendar(self, id):
        """Get calendar by id."""
        return self._calendars[id]

    def getDefaultCalendar(self):
        """Return the default calendar."""
        if not self._default_cal_class:
            return None
        return self._calendars[self._default_cal_class]

    def getCalendarClasses(self):
        """Return all defined calendar ids."""
        return self._calendars.keys()

    def setNumberFormat(self, klass, format, default=False):
        """Add a new number format for this locale."""
        self._number_formats[klass] = format
        if default:
            self._default_numformat_class = klass

    def getNumberFormat(self, klass):
        """Get number format by id."""
        return self._number_formats[klass]

    def getDefaultNumberFormat(self):
        """Return the default number format."""
        if not self._default_numformat_class:
            return None
        return self._number_formats[self._default_numformat_class]

    def getNumberFormatClasses(self):
        """Return all defined number format ids."""
        return self._number_formats.keys()

    def setCurrency(self, id, currency, default=False):
        """Add a new currency for this locale."""
        self._currencies[id] = currency
        if default:
            self._default_currency_id = id

    def getCurrency(self, id):
        """Get currency by id."""
        return self._currencies[id]

    def getDefaultCurrency(self):
        """Return the currency format."""
        if not self._default_currency_id:
            return None
        return self._currencies[self._default_currency_id]

    def getCurrencyIds(self):
        """Return all defined currency ids."""
        return self._currencies.keys()

    def _getNextLocale(self):
        """This is the really interesting method that looks up the next (more
        general) Locale object. This is used in case thi slocale object does
        not have the required information.

        This method works closely with with LocaleProvider.
        """
        language = self.id.getLanguage()
        country = self.id.getCountry()
        variant = self.id.getVariant()
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
        calendar = ICULocaleCalendar('gregorian')
        for id in ((None, None, None),
                   (self.id.getLanguage(), None, None),
                   (self.id.getLanguage(), self.id.getCountry(), None),
                   (self.id.getLanguage(), self.id.getCountry(),
                    self.id.getVariant())):
            try:
                calendar.update(locales.getLocale(*id).getCalendar(
                    'gregorian'))
            except KeyError:
                pass # Locale has no calendar information
        return calendar

    def getLocaleLanguageId(self):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        return self.id.getLanguage()

    def getLocaleCountryId(self):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        return self.id.getCountry()

    def getLocaleVariantId(self):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        return self.id.getVariant()

    def getDisplayLanguage(self, id):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            return self.getLanguageName(id)
        except KeyError:
            try:
                return self._getNextLocale().getDisplayLanguage(id)
            except NoGeneralLocaleError:
                raise KeyError, "Language '%s' not found." %id

    def getDisplayCountry(self, id):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            return self.getCountryName(id)
        except KeyError:
            try:
                return self._getNextLocale().getDisplayCountry(id)
            except NoGeneralLocaleError:
                raise KeyError, "Country '%s' not found." %id

    def getTimeFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().getTimePattern(name)
        except AttributeError, KeyError:
            return self._getNextLocale().getTimeFormatter(name)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getDateFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().getDatePattern(name)
        except AttributeError, KeyError:
            return self._getNextLocale().getDateFormatter(name)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getDateTimeFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultCalendar().getDateTimePattern()
        except AttributeError, KeyError:
            return self._getNextLocale().getDateTimeFormatter(name)
        date_pat = self.getDateFormatter(name).getPattern()
        time_pat = self.getTimeFormatter(name).getPattern()
        pattern = pattern.replace('{1}', date_pat)
        pattern = pattern.replace('{0}', time_pat)
        return DateTimeFormat(pattern, self._createFullCalendar())

    def getNumberFormatter(self, name):
        "See ZopeProducts.LocaleProvider.interfaces.ILocale"
        try:
            pattern = self.getDefaultNumberFormat().getPattern(name)
        except AttributeError, KeyError:
            return self._getNextLocale().getNumberFormatter(name)
        symbols = {}
        for id in ((None, None, None),
                   (self.id.getLanguage(), None, None),
                   (self.id.getLanguage(), self.id.getCountry(), None),
                   (self.id.getLanguage(), self.id.getCountry(),
                    self.id.getVariant())):
            try:
                format = locales.getLocale(*id).getDefaultNumberFormat()
                symbols.update(format.getSymbolMap())
            except AttributeError, KeyError:
                pass # Locale has no number format information

        return NumberFormat(pattern, symbols)

    def getDateFormat(self, name):
        """Get the DateFormat object called 'name'. The following names are
        recognized: full, long, medium, short."""
        raise NotImplementedError


class ICUXMLLocaleFactory:
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
        id = ICULocaleIdentity(**args)
        nodes = identity.getElementsByTagName('correspondsTo')
        for node in nodes:
            vendor = node.getAttribute('vendor')
            id.setCorrespondence(vendor, self._getText(node.childNodes))
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
            versions.append(ICULocaleVersion(id, date, comment))
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
            zone = ICULocaleTimeZone(id)
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
                    zone.setName(type, long_desc, short_desc)
            for city in node.getElementsByTagName('city'):
                zone.addCity(self._getText(city.childNodes))
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
            calendar.setMonth(id, names.get(id, None), abbr.get(id, None))

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
            calendar.setWeekday(id, name, abb)

    def _extractEras(self, cal_node, calendar):
        eras_node = cal_node.getElementsByTagName('eras')
        if eras_node:
            eras_node = eras_node[0]
            for era_node in eras_node.getElementsByTagName('era'):
                id = int(era_node.getAttribute('id'))
                calendar.setEra(id, self._getText(era_node.childNodes))

    def _extractCalendarPatterns(self, cal_node, calendar):
        try:
            pat_node = cal_node.getElementsByTagName('patterns')[0]
        except IndexError:
            return
        chars_node = pat_node.getElementsByTagName('chars')
        if chars_node:
            chars_node = chars_node[0]
            calendar.setPatternCharacters(
                self._getText(chars_node.childNodes))
        try:
            time_node = cal_node.getElementsByTagName('time')[0]
            date_node = cal_node.getElementsByTagName('date')[0]
        except IndexError:
            return
        for type in ('full', 'long', 'medium', 'short'):
            node = time_node.getElementsByTagName(type)[0]
            calendar.setTimePattern(type, self._getText(node.childNodes))
            node = date_node.getElementsByTagName(type)[0]
            calendar.setDatePattern(type, self._getText(node.childNodes))
        datetime_node = cal_node.getElementsByTagName('dateTime')[0]
        calendar.setDateTimePattern(self._getText(datetime_node.childNodes))

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
            calendar = ICULocaleCalendar(klass)
            default = cal_node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False
            nodes = cal_node.getElementsByTagName('am')
            if nodes:
                calendar.setAM(self._getText(nodes[0].childNodes))
            nodes = cal_node.getElementsByTagName('pm')
            if nodes:
                calendar.setPM(self._getText(nodes[0].childNodes))
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
            format = ICULocaleNumberFormat(klass)
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
                    format.setPattern(field,
                                      self._getText(field_node.childNodes))

            symbols_nodes = format_node.getElementsByTagName('symbols')
            if len(symbols_nodes) == 1:
                node = symbols_nodes[0]
                for field in ('decimal', 'group', 'list', 'percentSign',
                              'nativeZeroDigit', 'patternDigit', 'plusSign',
                              'minusSign', 'exponential', 'perMille',
                              'infinity', 'nan'):
                    try:
                        field_node = node.getElementsByTagName(field)[0]
                        format.setSymbol(field,
                                         self._getText(field_node.childNodes))
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
            currency = ICULocaleCurrency(id)
            default = curr_node.getAttribute('default')
            if default == u'true':
                default = True
            else:
                default = False
            node = curr_node.getElementsByTagName('symbol')[0]
            currency.setSymbol(self._getText(node.childNodes))
            node = curr_node.getElementsByTagName('name')[0]
            currency.setName(self._getText(node.childNodes))
            try:
                node = curr_node.getElementsByTagName('decimal')[0]
                currency.setDecimal(self._getText(node.childNodes))
            except IndexError:
                pass # No decimal node
            try:
                node = curr_node.getElementsByTagName('pattern')[0]
                currency.setPattern(self._getText(node.childNodes))
            except IndexError:
                pass # No pattern node

            currencies.append((id, currency, default))

        return currencies


    def __call__(self):
        """Create the Locale."""
        locale = ICULocale(self._extractIdentity())
        # Set Versioning
        for version in self._extractVersions():
            locale.setVersion(version)
        locale.updateLanguageNames(self._extractLanguages())
        locale.updateCountryNames(self._extractCountries())
        # Set TimeZones
        for tz in self._extractTimeZones():
            locale.setTimeZone(*tz)
        # Set Calendars
        for cal in self._extractCalendars():
            locale.setCalendar(*cal)
        # Set Number Formats
        for format in self._extractNumberFormats():
            locale.setNumberFormat(*format)
        # Set Currencies
        for currency in self._extractCurrencies():
            locale.setCurrency(*currency)

        return locale

