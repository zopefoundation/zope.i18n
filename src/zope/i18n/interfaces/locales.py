##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Interfaces related to Locales
"""
import re
from zope.interface import Interface, Attribute
from zope.schema import \
     Field, Text, TextLine, Int, Bool, Tuple, List, Dict, Date
from zope.schema import Container, Choice
from .._compat import _u

class ILocaleProvider(Interface):
    """This interface is our connection to the Zope 3 service. From it
    we can request various Locale objects that can perform all sorts of
    fancy operations.

    This service will be singelton global service, since it doe not make much
    sense to have many locale facilities, especially since this one will be so
    complete, since we will the ICU XML Files as data.  """

    def loadLocale(language=None, country=None, variant=None):
        """Load the locale with the specs that are given by the arguments of
        the method. Note that the LocaleProvider must know where to get the
        locales from."""

    def getLocale(language=None, country=None, variant=None):
        """Get the Locale object for a particular language, country and
        variant."""


class ILocaleIdentity(Interface):
    """Identity information class for ILocale objects.

    Three pieces of information are required to identify a locale:

      o language -- Language in which all of the locale text information are
        returned.

      o script -- Script in which all of the locale text information are
        returned.

      o territory -- Territory for which the locale's information are
        appropriate. None means all territories in which language is spoken.

      o variant -- Sometimes there are regional or historical differences even
        in a certain country. For these cases we use the variant field. A good
        example is the time before the Euro in Germany for example. Therefore
        a valid variant would be 'PREEURO'.

    Note that all of these attributes are read-only once they are set (usually
    done in the constructor)!

    This object is also used to uniquely identify a locale.
    """

    language = TextLine(
        title = _u("Language Type"),
        description = _u("The language for which a locale is applicable."),
        constraint = re.compile(r'[a-z]{2}').match,
        required = True,
        readonly = True)

    script = TextLine(
        title = _u("Script Type"),
        description = _u("""The script for which the language/locale is
                       applicable."""),
        constraint = re.compile(r'[a-z]*').match)

    territory = TextLine(
        title = _u("Territory Type"),
        description = _u("The territory for which a locale is applicable."),
        constraint = re.compile(r'[A-Z]{2}').match,
        required = True,
        readonly = True)

    variant = TextLine(
        title = _u("Variant Type"),
        description = _u("The variant for which a locale is applicable."),
        constraint = re.compile(r'[a-zA-Z]*').match,
        required = True,
        readonly = True)

    version = Field(
        title = _u("Locale Version"),
        description = _u("The value of this field is an ILocaleVersion object."),
        readonly = True)

    def __repr__(self):
        """Defines the representation of the id, which should be a compact
        string that references the language, country and variant."""


class ILocaleVersion(Interface):
    """Represents the version of a locale.

    The locale version is part of the ILocaleIdentity object.
    """

    number = TextLine(
        title = _u("Version Number"),
        description = _u("The version number of the locale."),
        constraint = re.compile(r'^([0-9].)*[0-9]$').match,
        required = True,
        readonly = True)

    generationDate = Date(
        title = _u("Generation Date"),
        description = _u("Specifies the creation date of the locale."),
        constraint = lambda date: date < datetime.now(),
        readonly = True)

    notes = Text(
        title = _u("Notes"),
        description = _u("Some release notes for the version of this locale."),
        readonly = True)


class ILocaleDisplayNames(Interface):
    """Localized Names of common text strings.

    This object contains localized strings for many terms, including
    language, script and territory names. But also keys and types used
    throughout the locale object are localized here.
    """

    languages = Dict(
        title = _u("Language type to translated name"),
        key_type = TextLine(title=_u("Language Type")),
        value_type = TextLine(title=_u("Language Name")))

    scripts = Dict(
        title = _u("Script type to script name"),
        key_type = TextLine(title=_u("Script Type")),
        value_type = TextLine(title=_u("Script Name")))

    territories = Dict(
        title = _u("Territory type to translated territory name"),
        key_type = TextLine(title=_u("Territory Type")),
        value_type = TextLine(title=_u("Territory Name")))

    variants = Dict(
        title = _u("Variant type to name"),
        key_type = TextLine(title=_u("Variant Type")),
        value_type = TextLine(title=_u("Variant Name")))

    keys = Dict(
        title = _u("Key type to name"),
        key_type = TextLine(title=_u("Key Type")),
        value_type = TextLine(title=_u("Key Name")))

    types = Dict(
        title = _u("Type type and key to localized name"),
        key_type = Tuple(title=_u("Type Type and Key")),
        value_type = TextLine(title=_u("Type Name")))


class ILocaleTimeZone(Interface):
    """Represents and defines various timezone information. It mainly manages
    all the various names for a timezone and the cities contained in it.

    Important: ILocaleTimeZone objects are not intended to provide
    implementations for the standard datetime module timezone support. They
    are merily used for Locale support.
    """

    type = TextLine(
        title = _u("Time Zone Type"),
        description = _u("Standard name of the timezone for unique referencing."),
        required = True,
        readonly = True)

    cities = List(
        title = _u("Cities"),
        description = _u("Cities in Timezone"),
        value_type = TextLine(title=_u("City Name")),
        required = True,
        readonly = True)


    names = Dict(
        title = _u("Time Zone Names"),
        description = _u("Various names of the timezone."),
        key_type = Choice(
                   title = _u("Time Zone Name Type"),
                   values = (_u("generic"), _u("standard"), _u("daylight"))),
        value_type = Tuple(title=_u("Time Zone Name and Abbreviation"),
                           min_length=2, max_length=2),
        required = True,
        readonly = True)


class ILocaleFormat(Interface):
    """Specifies a format for a particular type of data."""

    type = TextLine(
        title=_u("Format Type"),
        description=_u("The name of the format"),
        required = False,
        readonly = True)

    displayName = TextLine(
        title = _u("Display Name"),
        description = _u("Name of the calendar, for example 'gregorian'."),
        required = False,
        readonly = True)

    pattern = TextLine(
        title = _u("Format Pattern"),
        description = _u("The pattern that is used to format the object."),
        required = True,
        readonly = True)


class ILocaleFormatLength(Interface):
    """The format length describes a class of formats."""

    type = Choice(
        title = _u("Format Length Type"),
        description = _u("Name of the format length"),
        values = (_u("full"), _u("long"), _u("medium"), _u("short"))
        )

    default = TextLine(
        title=_u("Default Format"),
        description=_u("The name of the defaulkt format."))

    formats = Dict(
        title = _u("Formats"),
        description = _u("Maps format types to format objects"),
        key_type = TextLine(title = _u("Format Type")),
        value_type = Field(
                         title = _u("Format Object"),
                         description = _u("Values are ILocaleFormat objects.")),
        required = True,
        readonly = True)


class ILocaleMonthContext(Interface):
    """Specifices a usage context for month names"""

    type = TextLine(
        title=_u("Month context type"),
        description=_u("Name of the month context, format or stand-alone."))

    defaultWidth = TextLine(
        title=_u("Default month name width"),
        default=_u("wide"))

    months = Dict(
        title=_u("Month Names"),
        description=_u("A mapping of month name widths to a mapping of"
                       "corresponding month names."),
        key_type=Choice(
            title=_u("Width type"),
            values=(_u("wide"), _u("abbreviated"), _u("narrow"))),
        value_type=Dict(
            title=_u("Month name"),
            key_type=Int(title=_u("Type"), min=1, max=12),
            value_type=TextLine(title=_u("Month Name")))
        )


class ILocaleDayContext(Interface):
    """Specifices a usage context for days names"""

    type = TextLine(
        title=_u("Day context type"),
        description=_u("Name of the day context, format or stand-alone."))

    defaultWidth = TextLine(
        title=_u("Default day name width"),
        default=_u("wide"))

    days = Dict(
        title=_u("Day Names"),
        description=_u("A mapping of day name widths to a mapping of"
                       "corresponding day names."),
        key_type=Choice(
            title=_u("Width type"),
            values=(_u("wide"), _u("abbreviated"), _u("narrow"))),
        value_type=Dict(
            title=_u("Day name"),
            key_type=Choice(
                title=_u("Type"),
                values=(_u("sun"), _u("mon"), _u("tue"), _u("wed"),
                        _u("thu"), _u("fri"), _u("sat"))),
            value_type=TextLine(title=_u("Day Name")))
        )


class ILocaleCalendar(Interface):
    """There is a massive amount of information contained in the calendar,
    which made it attractive to be added."""

    type = TextLine(
        title=_u("Calendar Type"),
        description=_u("Name of the calendar, for example 'gregorian'."))

    defaultMonthContext = TextLine(
        title=_u("Default month context"),
        default=_u("format"))

    monthContexts = Dict(
        title=_u("Month Contexts"),
        description=_u("A mapping of month context types to "
                       "ILocaleMonthContext objects"),
        key_type=Choice(title=_u("Type"),
                        values=(_u("format"), _u("stand-alone"))),
        value_type=Field(title=_u("ILocaleMonthContext object")))

    # BBB: leftover from CLDR 1.0
    months = Dict(
        title = _u("Month Names"),
        description = _u("A mapping of all month names and abbreviations"),
        key_type = Int(title=_u("Type"), min=1, max=12),
        value_type = Tuple(title=_u("Month Name and Abbreviation"),
                           min_length=2, max_length=2))

    defaultDayContext = TextLine(
        title=_u("Default day context"),
        default=_u("format"))

    dayContexts = Dict(
        title=_u("Day Contexts"),
        description=_u("A mapping of day context types to "
                       "ILocaleDayContext objects"),
        key_type=Choice(title=_u("Type"),
                        values=(_u("format"), _u("stand-alone"))),
        value_type=Field(title=_u("ILocaleDayContext object")))

    # BBB: leftover from CLDR 1.0
    days = Dict(
        title=_u("Weekdays Names"),
        description = _u("A mapping of all month names and abbreviations"),
        key_type = Choice(title=_u("Type"),
                            values=(_u("sun"), _u("mon"), _u("tue"), _u("wed"),
                                    _u("thu"), _u("fri"), _u("sat"))),
        value_type = Tuple(title=_u("Weekdays Name and Abbreviation"),
                           min_length=2, max_length=2))

    week = Dict(
        title=_u("Week Information"),
        description = _u("Contains various week information"),
        key_type = Choice(
            title=_u("Type"),
            description=_u("""
            Varies Week information:

              - 'minDays' is just an integer between 1 and 7.

              - 'firstDay' specifies the first day of the week by integer.

              - The 'weekendStart' and 'weekendEnd' are tuples of the form
                (weekDayNumber, datetime.time)
            """),
            values=(_u("minDays"), _u("firstDay"),
                    _u("weekendStart"), _u("weekendEnd"))))

    am = TextLine(title=_u("AM String"))

    pm = TextLine(title=_u("PM String"))

    eras = Dict(
        title = _u("Era Names"),
        key_type = Int(title=_u("Type"), min=0),
        value_type = Tuple(title=_u("Era Name and Abbreviation"),
                           min_length=2, max_length=2))

    defaultDateFormat = TextLine(title=_u("Default Date Format Type"))

    dateFormats = Dict(
        title=_u("Date Formats"),
        description = _u("Contains various Date Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    defaultTimeFormat = TextLine(title=_u("Default Time Format Type"))

    timeFormats = Dict(
        title=_u("Time Formats"),
        description = _u("Contains various Time Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    defaultDateTimeFormat = TextLine(title=_u("Default Date-Time Format Type"))

    dateTimeFormats = Dict(
        title=_u("Date-Time Formats"),
        description = _u("Contains various Date-Time Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    def getMonthNames():
        """Return a list of month names."""

    def getMonthTypeFromName(name):
        """Return the type of the month with the right name."""

    def getMonthAbbreviations():
        """Return a list of month abbreviations."""

    def getMonthTypeFromAbbreviation(abbr):
        """Return the type of the month with the right abbreviation."""

    def getDayNames():
        """Return a list of weekday names."""

    def getDayTypeFromName(name):
        """Return the id of the weekday with the right name."""

    def getDayAbbr():
        """Return a list of weekday abbreviations."""

    def getDayTypeFromAbbr(abbr):
        """Return the id of the weekday with the right abbr."""

    def isWeekend(datetime):
        """Determines whether a the argument lies in a weekend."""

    def getFirstDayName():
        """Return the the type of the first day in the week."""


class ILocaleDates(Interface):
    """This object contains various data about dates, times and time zones."""

    localizedPatternChars = TextLine(
        title = _u("Localized Pattern Characters"),
        description = _u("Localized pattern characters used in dates and times"))

    calendars = Dict(
        title = _u("Calendar type to ILocaleCalendar"),
        key_type = Choice(
            title=_u("Calendar Type"),
            values=(_u("gregorian"),
                            _u("arabic"),
                            _u("chinese"),
                            _u("civil-arabic"),
                            _u("hebrew"),
                            _u("japanese"),
                            _u("thai-buddhist"))),
        value_type=Field(title=_u("Calendar"),
                         description=_u("This is a ILocaleCalendar object.")))

    timezones = Dict(
        title=_u("Time zone type to ILocaleTimezone"),
        key_type=TextLine(title=_u("Time Zone type")),
        value_type=Field(title=_u("Time Zone"),
                         description=_u("This is a ILocaleTimeZone object.")))

    def getFormatter(category, length=None, name=None, calendar=_u("gregorian")):
        """Get a date/time formatter.

        `category` must be one of 'date', 'dateTime', 'time'.

        The 'length' specifies the output length of the value. The allowed
        values are: 'short', 'medium', 'long' and 'full'. If no length was
        specified, the default length is chosen.
        """


class ILocaleCurrency(Interface):
    """Defines a particular currency."""

    type = TextLine(title=_u("Type"))

    symbol = TextLine(title=_u("Symbol"))

    displayName = TextLine(title=_u("Official Name"))

    symbolChoice = Bool(title=_u("Symbol Choice"))

class ILocaleNumbers(Interface):
    """This object contains various data about numbers and currencies."""

    symbols = Dict(
        title = _u("Number Symbols"),
        key_type = Choice(
            title = _u("Format Name"),
            values = (_u("decimal"), _u("group"), _u("list"), _u("percentSign"),
                      _u("nativeZeroDigit"), _u("patternDigit"), _u("plusSign"),
                      _u("minusSign"), _u("exponential"), _u("perMille"),
                      _u("infinity"), _u("nan"))),
        value_type=TextLine(title=_u("Symbol")))

    defaultDecimalFormat = TextLine(title=_u("Default Decimal Format Type"))

    decimalFormats = Dict(
        title=_u("Decimal Formats"),
        description = _u("Contains various Decimal Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    defaultScientificFormat = TextLine(title=_u("Default Scientific Format Type"))

    scientificFormats = Dict(
        title=_u("Scientific Formats"),
        description = _u("Contains various Scientific Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    defaultPercentFormat = TextLine(title=_u("Default Percent Format Type"))

    percentFormats = Dict(
        title=_u("Percent Formats"),
        description = _u("Contains various Percent Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    defaultCurrencyFormat = TextLine(title=_u("Default Currency Format Type"))

    currencyFormats = Dict(
        title=_u("Currency Formats"),
        description = _u("Contains various Currency Formats."),
        key_type = Choice(
                      title=_u("Type"),
                      description = _u("Name of the format length"),
                      values = (_u("full"), _u("long"), _u("medium"), _u("short"))),
        value_type = Field(title=_u("ILocaleFormatLength object")))

    currencies = Dict(
        title=_u("Currencies"),
        description = _u("Contains various Currency data."),
        key_type = TextLine(
                      title=_u("Type"),
                      description = _u("Name of the format length")),
        value_type = Field(title=_u("ILocaleCurrency object")))


    def getFormatter(category, length=None, name=_u("")):
        """Get the NumberFormat based on the category, length and name of the
        format.

        The 'category' specifies the type of number format you would like to
        have. The available options are: 'decimal', 'percent', 'scientific',
        'currency'.

        The 'length' specifies the output length of the number. The allowed
        values are: 'short', 'medium', 'long' and 'full'. If no length was
        specified, the default length is chosen.

        Every length can have actually several formats. In this case these
        formats are named and you can specify the name here. If no name was
        specified, the first unnamed format is chosen.
        """

    def getDefaultCurrency():
        """Get the default currency."""

_orientations = [_u("left-to-right"), _u("right-to-left"),
                 _u("top-to-bottom"), _u("bottom-to-top")]
class ILocaleOrientation(Interface):
    """Information about the orientation of text."""

    characters = Choice(
        title = _u("Orientation of characters"),
        values = _orientations,
        default = _u("left-to-right")
        )

    lines = Choice(
        title = _u("Orientation of characters"),
        values = _orientations,
        default = _u("top-to-bottom")
        )

class ILocale(Interface):
    """This class contains all important information about the locale.

    Usually a Locale is identified using a specific language, country and
    variant.  However, the country and variant are optional, so that a lookup
    hierarchy develops.  It is easy to recognize that a locale that is missing
    the variant is more general applicable than the one with the variant.
    Therefore, if a specific Locale does not contain the required information,
    it should look one level higher.  There will be a root locale that
    specifies none of the above identifiers.
    """

    id = Field(
        title = _u("Locale identity"),
        description = _u("ILocaleIdentity object identifying the locale."),
        required = True,
        readonly = True)

    displayNames = Field(
        title = _u("Display Names"),
        description = _u("""ILocaleDisplayNames object that contains localized
                        names."""))

    dates = Field(
        title = _u("Dates"),
        description = _u("ILocaleDates object that contains date/time data."))

    numbers = Field(
        title = _u("Numbers"),
        description = _u("ILocaleNumbers object that contains number data."))

    orientation = Field(
        title = _u("Orientation"),
        description = _u("ILocaleOrientation with text orientation info."))

    delimiters = Dict(
        title=_u("Delimiters"),
        description = _u("Contains various Currency data."),
        key_type = Choice(
            title=_u("Delimiter Type"),
            description = _u("Delimiter name."),
            values=(_u("quotationStart"),
                    _u("quotationEnd"),
                    _u("alternateQuotationStart"),
                    _u("alternateQuotationEnd"))),
        value_type = Field(title=_u("Delimiter symbol")))

    def getLocaleID():
        """Return a locale id as specified in the LDML specification"""


class ILocaleInheritance(Interface):
    """Locale inheritance support.

    Locale-related objects implementing this interface are able to ask for its
    inherited self. For example, 'en_US.dates.monthNames' can call on itself
    'getInheritedSelf()' and get the value for 'en.dates.monthNames'.
    """

    __parent__ = Attribute("The parent in the location hierarchy")

    __name__ = TextLine(
        title = _u("The name within the parent"),
        description=_u("""The parent can be traversed with this name to get
                       the object."""))

    def getInheritedSelf():
        """Return itself but in the next higher up Locale."""


class IAttributeInheritance(ILocaleInheritance):
    """Provides inheritance properties for attributes"""

    def __setattr__(name, value):
        """Set a new attribute on the object.

        When a value is set on any inheritance-aware object and the value
        also implements ILocaleInheritance, then we need to set the
        '__parent__' and '__name__' attribute on the value.
        """

    def __getattribute__(name):
        """Return the value of the attribute with the specified name.

        If an attribute is not found or is None, the next higher up Locale
        object is consulted."""


class IDictionaryInheritance(ILocaleInheritance):
    """Provides inheritance properties for dictionary keys"""

    def __setitem__(key, value):
        """Set a new item on the object.

        Here we assume that the value does not require any inheritance, so
        that we do not set '__parent__' or '__name__' on the value.
        """

    def __getitem__(key):
        """Return the value of the item with the specified name.

        If an key is not found or is None, the next higher up Locale
        object is consulted.
        """

class ICollator(Interface):
    """Provide support for collating text strings

    This interface will typically be provided by adapting a locale.
    """

    def key(text):
        """Return a collation key for the given text.
        """

    def cmp(text1, text2):
        """Compare two text strings.

        The return value is negative if text1 < text2, 0 is they are
        equal, and positive if text1 > text2.
        """
