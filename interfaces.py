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
"""Internationalization of content objects.

$Id: interfaces.py,v 1.11 2003/04/11 12:47:42 mgedmin Exp $
"""
import re
from zope.interface import Interface, Attribute
from zope.schema import TextLine, Text, Int, Dict, Tuple, List
from zope.schema import Container, Datetime


class II18nAware(Interface):
    """Internationalization aware content object."""

    def getDefaultLanguage():
        """Return the default language."""

    def setDefaultLanguage(language):
        """Set the default language, which will be used if the language is not
        specified, or not available.
        """

    def getAvailableLanguages():
        """Find all the languages that are available."""


class IMessageCatalog(Interface):
    """A catalog (mapping) of message ids to message text strings.

    This interface provides a method for translating a message or message id,
    including text with interpolation.  The message catalog basically serves
    as a fairly simple mapping object.

    A single message catalog represents a specific language and domain.
    Therefore you will have the following constructor arguments:

    language -- The language of the returned messages.  This is a read-only
                attribute.

    domain -- The translation domain for these messages.  This is a read-only
              attribute.  See ITranslationService.

    When we refer to text here, we mean text that follows the standard Zope 3
    text representation.

    Note: The IReadMessageCatalog is the absolut minimal version required for
          the TranslationService to function.
    """

    def getMessage(msgid):
        """Get the appropriate text for the given message id.

        An exception is raised if the message id is not found.
        """

    def queryMessage(msgid, default=None):
        """Look for the appropriate text for the given message id.

        If the message id is not found, default is returned.
        """

    def getLanguage():
        """Return the language this message catalog is representing."""

    def getDomain():
        """Return the domain this message catalog is serving."""

    def getIdentifier():
        """Return a identifier for this message catalog. Note that this
        identifier does not have to be unique as several message catalog
        could serve the same domain and language.

        Also, there are no restrictions on the form of the identifier.
        """


class ITranslationService(Interface):
    """The Translation Service

    This interface provides methods for translating text, including text with
    interpolation.

    When we refer to text here, we mean text that follows the standard Zope 3
    text representation.

    Standard arguments in the methods described below:

        domain -- The domain is used to specify which translation to use.
                  Different products will often use a specific domain naming
                  translations supplied with the product.

                  A favorite example is: How do you translate "Sun"?  Is it
                  our star, the abbreviation of Sunday or the company?
                  Specifying the domain, such as "Stars" or "DaysOfWeek" will
                  solve this problem for us.

        msgid -- The id of the message that should be translated.  This may be
                 an implicit or an explicit message id.

        mapping -- The object to get the interpolation data from.

        target_language -- The language to translate to.

        context -- An object that provides contextual information for
                   determining client language preferences.  It must implement
                   or have an adapter that implements IUserPreferredLanguages.

        Note that one of target_language or context must be passed.  Otherwise
        a TypeError will be raised.

        Also note that language tags are defined by RFC 1766.
    """

    def translate(domain, msgid, mapping=None,
                  context=None, target_language=None,
                  default=None):
        """Return the translation for the message referred to by msgid.

        Return the default if no translation is found.

        However, the method does a little more than a vanilla translation.
        The method also looks for a possible language to translate to.
        After a translation it also replaces any $name variable variables
        inside the post-translation string.

        Note: The TranslationService interface does not support simplified
        translation methods, since it is totally hidden by ZPT and in
        Python you should use a Domain object, since it supports all
        the simplifications.
        """


class ITranslator(Interface):
    """A collaborative object which contains the domain, context, and locale.

    It is expected that object be constructed with enough information to find
    the domain, context, and target language.
    """

    def translate(msgid, mapping=None):
        """Translate the source msgid using the given mapping.

        See ITranslationService for details.
        """


class IMessageImportFilter(Interface):
    """The Import Filter for Translation Service Messages.

       Classes implementing this interface should usually be Adaptors, as
       they adapt the IEditableTranslationService interface."""


    def importMessages(domains, languages, file):
        """Import all messages that are defined in the specified domains and
           languages.

           Note that some implementations might limit to only one domain and
           one language. A good example for that is a GettextFile.
        """


class ILanguageAvailability(Interface):

    def getAvailableLanguages():
        """Return a sequence of language tags for available languages
        """


class IUserPreferredLanguages(Interface):

    """This interface provides language negotiation based on user preferences.
    """

    def getPreferredLanguages():
        """Return a sequence of user preferred languages.
        """


class IMessageExportFilter(Interface):
    """The Export Filter for Translation Service Messages.

       Classes implementing this interface should usually be Adaptors, as
       they adapt the IEditableTranslationService interface."""


    def exportMessages(domains, languages):
        """Export all messages that are defined in the specified domains and
           languages.

           Note that some implementations might limit to only one domain and
           one language. A good example for that is a GettextFile.
        """


class INegotiator(Interface):
    """A language negotiation service.
    """

    def getLanguage(langs, env):
        """Return the matching language to use.

        The decision of which language to use is based on the list of
        available languages, and the given user environment.  An
        IUserPreferredLanguages adapter for the environment is obtained and
        the list of acceptable languages is retrieved from the environment.

        If no match is found between the list of available languages and the
        list of acceptable languages, None is returned.

        Arguments:

        langs -- sequence of languages (not necessarily ordered)

        env  -- environment passed to the service to determine a sequence
                of user prefered languages
        """

        # XXX I'd like for there to be a symmetric interface method, one in
        # which an adapter is gotten for both the first arg and the second
        # arg.  I.e. getLanguage(obj, env)
        # But this isn't a good match for the ITranslationService.translate()
        # method. :(


class IUserPreferredCharsets(Interface):
    """This interface provides charset negotiation based on user preferences.
    """

    def getPreferredCharsets():
        """Return a sequence of user preferred charsets. Note that the order
           should describe the order of preference. Therefore the first
           character set in the list is the most preferred one.
        """


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

      o language -- Language in which all of the locale txt information are
        returned.

      o country -- Country for which the locale's information are
        appropriate. None means all countries in which language is spoken.

      o variant -- Sometimes there are regional or historical differences even
        in a certain country. For these cases we use the variant field. A good
        example is the time before the Euro in Germany for example. Therefore
        a valid variant would be 'PREEURO'.

    Note that all of these attributes are read-only once they are set (usually
    done in constructor)!

    This object is also used to uniquely identify a locale."""

    language = TextLine(title=u"Language Id",
                        constraint=re.compile(r'[a-z]{2}').match)

    country = TextLine(title=u"Country Id",
                        constraint=re.compile(r'[A-Z]{2}').match)

    variant = TextLine(title=u"Variant",
                        constraint=re.compile(r'[a-zA-Z]*').match)


    correspondsTo = List(title=u"Corresponds to",
                         description=u"""'Corresponds to' can be used to map
                         our Locales to other system's locales. A common use
                         in ICU is to define a correspondence to the Windows
                         Locale System.""",
                         value_types=(Tuple(title=u"Vendor-Signature Pair",
                                            min_length=2, max_length=2),))

    def __repr__(self):
        """Defines the representation of the id, which should be a compact
        string that references the language, country and variant."""


class ILocaleVersion(Interface):
    """Allows one to specify a version of a locale."""

    id = TextLine(title=u"Version identifier; usually something like 1.0.1",
                  constraint=re.compile(r'[0-9\.]*').match)

    date = Datetime(
        title=u"A datetime object specifying the version creation date.")

    comment = Text(title=u"A text comment about the version.")

    def __cmp__(other):
        """Compares versions, so the order can be determined."""


class ILocaleTimeZone(Interface):
    """Represents and defines various timezone information. It mainly manages
    all the various names for a timezone and the cities contained in it.

    Important: ILocaleTimeZone objects are not intended to provide
    implementations for the standard datetime module timezone support. They
    are merily used for Locale support.
    """

    id = TextLine(
        title=u"Time Zone Id",
        description=u"Standard name of the timezone for unique referencing.")

    cities = List(title=u"Cities", description=u"Cities in Timezone",
                  value_types=(TextLine(title=u"City Name"),))

    names = Dict(
        title=u"Time Zone Names",
        key_types=(TextLine(title=u"Time Zone Name Type",
                            allowed_values=(u'generic', u'standard',
                                            u'daylight')),),
        value_types=(TextLine(title=u"Time Zone Name"),))


class ILocaleCalendar(Interface):
    """There is a massive amount of information contained in the calendar,
    which made it attractive to be added """

    months = Dict(title=u"Month Names",
                  key_types=(Int(title=u"Id", min=1, max=12),),
                  value_types=(Tuple(title=u"Month Name and Abbreviation",
                  min_length=2, max_length=2),))

    weekdays = Dict(title=u"Weekdays Names",
                  key_types=(Int(title=u"Id", min=1, max=7),),
                  value_types=(Tuple(title=u"Weekdays Name and Abbreviation",
                  min_length=2, max_length=2),))

    eras = Dict(title=u"Era Names",
                  key_types=(Int(title=u"Id", min=1, max=2),),
                  value_types=(TextLine(title=u"Era Name"),))

    am = TextLine(title=u"AM String")

    pm = TextLine(title=u"PM String")

    patternCharacters = TextLine(title=u"Pattern Characters")

    timePatterns = Dict(
        title=u"Time Patterns",
        key_types=(TextLine(title=u"Pattern Name",
                            allowed_values=(u'full', u'long',
                                            u'medium', u'short')),),
        value_types=(TextLine(title=u"Time Pattern"),))

    datePatterns = Dict(
        title=u"Date Patterns",
        key_types=(TextLine(title=u"Pattern Name",
                            allowed_values=(u'full', u'long',
                                            u'medium', u'short')),),
        value_types=(TextLine(title=u"Date Pattern"),))

    dateTimePattern = Dict(title=u"Date-Time Pattern",
                           value_types=(TextLine(title=u"Pattern"),))

    def update(other):
        """Update this calendar using data from other. Assume that unless
        other's data is not present, other has always more specific
        information."""

    def getMonthNames():
        """Return a list of month names."""

    def getMonthIdFromName(name):
        """Return the id of the month with the right name."""

    def getMonthAbbr():
        """Return a list of month abbreviations."""

    def getMonthIdFromAbbr(abbr):
        """Return the id of the month with the right abbreviation."""

    def getWeekdayNames():
        """Return a list of weekday names."""

    def getWeekdayIdFromName(name):
        """Return the id of the weekday with the right name."""

    def getWeekdayAbbr():
        """Return a list of weekday abbreviations."""

    def getWeekdayIdFromAbbr(abbr):
        """Return the id of the weekday with the right abbr."""


class ILocaleNumberFormat(Interface):
    """This interface defines all the formatting information for one class of
    numbers."""

    patterns = Dict(
        title=u"Number Patterns",
        key_types=(TextLine(title=u"Format Name",
                            allowed_values=(u'decimal', u'percent',
                                            u'scientific')),),
        value_types=(TextLine(title=u"Pattern"),))

    symbols = Dict(
        title=u"Number Symbols",
        key_types=(TextLine(title=u"Format Name",
                           allowed_values=(u'decimal', u'group', u'list',
                                           u'percentSign', u'nativeZeroDigit',
                                           u'patternDigit', u'plusSign',
                                           u'minusSign', u'exponential',
                                           u'perMille', u'infinity',
                                           u'nan')),),
        value_types=(TextLine(title=u"Symbol"),))


class ILocaleCurrency(Interface):
    """Defines a particular currency."""

    symbol = TextLine(title=u'Symbol')

    name = TextLine(title=u'Name')

    decimal = TextLine(title=u'Decimal Symbol')

    pattern = TextLine(title=u'Pattern',
                    description=u"""Set currency pattern. Often we want
                    different formatting rules for monetary amounts; for
                    example a precision more than 1/100 of the main currency
                    unit is often not desired.""")

    formatter = Attribute("Currency Formatter object")


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

    id = Attribute("""ILocaleIdentity object identifying the locale.""")

    currencies = Container(title=u"Currencies")

    languages = Dict(title=u"Language id to translated name",
                     key_types=(TextLine(title=u"Language Id"),),
                     value_types=(TextLine(title=u"Language Name"),),
                     )

    countries = Dict(title=u"Country id to translated name",
                     key_types=(TextLine(title=u"Country Id"),),
                     value_types=(TextLine(title=u"Country Name"),),
                     )

    timezones = Dict(title=u"Time zone id to ITimezone",
                     key_types=(TextLine(title=u"Time Zone Id"),),
                     )

    calendars = Dict(title=u"Calendar id to ICalendar",
                     key_types=(TextLine(title=u"Calendar Id"),),
                     )

    def getDefaultTimeZone():
        """Return the default time zone."""

    def getDefaultCalendar():
        """Return the default calendar."""

    def getDefaultNumberFormat():
        """Return the default number format."""

    def getDefaultCurrency():
        """Get the default currency."""

    def getDisplayLanguage(id):
        """Return the full name of the language whose id was passed in the
        language of this locale."""

    def getDisplayCountry(id):
        """Return the full name of the country of this locale."""

    def getTimeFormatter(name):
        """Get the TimeFormat object called 'name'. The following names are
        recognized: full, long, medium, short."""

    def getDateFormatter(name):
        """Get the DateFormat object called 'name'. The following names are
        recognized: full, long, medium, short."""

    def getDateTimeFormatter(name):
        """Get the DateTimeFormat object called 'name'. The following names
        are recognized: full, long, medium, short."""

    def getNumberFormatter(name):
        """Get the NumberFormat object called 'name'. The following names are
        recognized: decimal, percent, scientific, currency."""



class IFormat(Interface):
    """A generic formatting class. It basically contains the parsing and
    construction method for the particular object the formatting class
    handles.

    The constructor will always require a pattern (specific to the object).
    """

    def setPattern(pattern):
        """Overwrite the old formatting pattern with the new one."""

    def getPattern():
        """Get the currently used pattern."""

    def parse(text, pattern=None):
        """Parse the text and convert it to an object, which is returned."""

    def format(obj, pattern=None):
        """Format an object to a string using the pattern as a rule."""



class INumberFormat(IFormat):
    u"""Specific number formatting interface. Here are the formatting
    rules (I modified the rules from ICU a bit, since I think they did not
    agree well with the real world XML formatting strings):

      posNegPattern      := ({subpattern};{subpattern} | {subpattern})
      subpattern         := {padding}{prefix}{padding}{integer}{fraction}
                            {exponential}{padding}{suffix}{padding}
      prefix             := '\u0000'..'\uFFFD' - specialCharacters *
      suffix             := '\u0000'..'\uFFFD' - specialCharacters *
      integer            := {digitField}'0'
      fraction           := {decimalPoint}{digitField}
      exponential        := E integer
      digitField         := ( {digitField} {groupingSeparator} |
                              {digitField} '0'* |
                              '0'* |
                              {optionalDigitField} )
      optionalDigitField := ( {digitField} {groupingSeparator} |
                              {digitField} '#'* |
                              '#'* )
      groupingSeparator  := ,
      decimalPoint       := .
      padding            := * '\u0000'..'\uFFFD'


    Possible pattern symbols:

      0    A digit. Always show this digit even if the value is zero.
      #    A digit, suppressed if zero
      .    Placeholder for decimal separator
      ,    Placeholder for grouping separator
      E    Separates mantissa and exponent for exponential formats
      ;    Separates formats (that is, a positive number format verses a
           negative number format)
      -    Default negative prefix. Note that the locale's minus sign
           character is used.
      +    If this symbol is specified the locale's plus sign character is
           used.
      %    Multiply by 100, as percentage
      ?    Multiply by 1000, as per mille
      \u00A4    This is the currency sign. it will be replaced by a currency
           symbol. If it is present in a pattern, the monetary decimal
           separator is used instead of the decimal separator.
      \u00A4\u00A4   This is the international currency sign. It will be replaced
           by an international currency symbol.  If it is present in a
           pattern, the monetary decimal separator is used instead of
           the decimal separator.
      X    Any other characters can be used in the prefix or suffix
      '    Used to quote special characters in a prefix or suffix
    """

    symbols = Dict(
        title=u"Number Symbols",
        key_types=(TextLine(
            title=u"Dictionary Class",
            allowed_values=(u'decimal', u'group', u'list', u'percentSign',
                            u'nativeZeroDigit', u'patternDigit', u'plusSign',
                            u'minusSign', u'exponential', u'perMille',
                            u'infinity', u'nan')),),
        value_types=(TextLine(title=u"Symbol"),))


class ICurrencyFormat(INumberFormat):
    """Special currency parsing class."""

    currency = Attribute("""This object must implement ILocaleCurrency. See
                            this interface's documentation for details.""")


class IDateTimeFormat(IFormat):
    """DateTime formatting and parsing interface. Here is a list of
    possible characters and their meaning:

      Symbol Meaning               Presentation      Example

      G      era designator        (Text)            AD
      y      year                  (Number)          1996
      M      month in year         (Text and Number) July and 07
      d      day in month          (Number)          10
      h      hour in am/pm (1~12)  (Number)          12
      H      hour in day (0~23)    (Number)          0
      m      minute in hour        (Number)          30
      s      second in minute      (Number)          55
      S      millisecond           (Number)          978
      E      day in week           (Text)            Tuesday
      D      day in year           (Number)          189
      F      day of week in month  (Number)          2 (2nd Wed in July)
      w      week in year          (Number)          27
      W      week in month         (Number)          2
      a      am/pm marker          (Text)            pm
      k      hour in day (1~24)    (Number)          24
      K      hour in am/pm (0~11)  (Number)          0
      z      time zone             (Text)            Pacific Standard Time
      '      escape for text
      ''     single quote                            '

    Meaning of the amount of characters:

      Text

        Four or more, use full form, <4, use short or abbreviated form if it
        exists. (for example, "EEEE" produces "Monday", "EEE" produces "Mon")

      Number

        The minimum number of digits. Shorter numbers are zero-padded to this
        amount (for example, if "m" produces "6", "mm" produces "06"). Year is
        handled specially; that is, if the count of 'y' is 2, the Year will be
        truncated to 2 digits. (for example, if "yyyy" produces "1997", "yy"
        produces "97".)

      Text and Number

        Three or over, use text, otherwise use number. (for example, "M"
        produces "1", "MM" produces "01", "MMM" produces "Jan", and "MMMM"
        produces "January".)  """

    calendar = Attribute("""This object must implement ILocaleCalendar. See
                            this interface's documentation for details.""")


