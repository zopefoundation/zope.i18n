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

$Id: interfaces.py,v 1.1 2002/12/31 02:52:13 jim Exp $
"""

from zope.interface import Interface

class II18nAware(Interface):
    """Internationalization aware content object.
    """

    def getDefaultLanguage():
        """Return the default language."""

    def setDefaultLanguage(language):
        """Set the default language, which will be used if the language is not
        specified, or not available.
        """

    def getAvailableLanguages():
        """Find all the languages that are available."""


class IReadMessageCatalog(Interface):
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


class IWriteMessageCatalog(Interface):
    """If this interfaces is implemented by a message catalog, then we will be
    able to update our messages.

    Note that not all methods here require write access, but they should
    not be required for an IReadMEssageCatalog and are used for editing
    only. Therefore this is the more suitable interface to put them.
    """

    def getFullMessage(msgid):
        """Get the message data and meta data as a nice dictionary. More
        advanced implementation might choose to return an object with
        the data, but the object should then implement IEnumerableMapping.

        An exception is raised if the message id is not found.
        """

    def setMessage(msgid, message, mod_time=None):
        """Set a message to the catalog. If mod_time is None use the current
           time instead as modification time."""

    def deleteMessage(msgid):
        """Delete a message from the catalog."""

    def getMessageIds():
        """Get a list of all the message ids."""

    def getMessages():
        """Get a list of all the messages."""


class IMessageCatalog(IReadMessageCatalog, IWriteMessageCatalog):
    """Most message catalogs should support this interface.
    """


class IReadTranslationService(Interface):
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
                  context=None, target_language=None):
        """Return the translation for the message referred to by msgid.

        Return None if no translation is found.

        However, the method does a little more than a vanilla translation.
        The method also looks for a possible language to translate to.
        After a translation it also replaces any $name variable variables
        inside the post-translation string.

        Note: The TranslationService interface does not support simplified
        translation methods, since it is totally hidden by ZPT and in
        Python you should use a Domain object, since it supports all
        the simplifications.
        """

    def getDomain(domain):
        """Get the domain for the passed domain name.

        The domain supports the IDomain interface
        """


class IWriteTranslationService(Interface):
    """This interface describes the methods that are necessary for an editable
    Translation Service to work.

    For a translation service to be editable its 'messages' have to support
    the following information: id, string, domain, language, date

    Most of the information will be natural, since they are required by the
    translation service, but especially the date is not a necessary info
    (in fact, it is meta data)
    """

    def getMessageIdsOfDomain(domain, filter='%'):
        """Get all the message ids of a particular domain."""

    def getMessagesOfDomain(domain):
        """Get all the messages of a particular domain."""

    def getMessage(msgid, domain, langauge):
        """Get the full message of a particular domain and language."""

    def getAllLanguages():
        """Find all the languages that are available"""

    def getAllDomains():
        """Find all available domains."""

    def getAvailableLanguages(domain):
        """Find all the languages that are available for this domain"""

    def getAvailableDomains(language):
        """Find all available domains."""

    def addMessage(domain, msgid, msg, language, mod_time=None):
        """Add a message to the translation service.

        If mod_time is None, then the current time should be inserted.
        """

    def updateMessage(domain, msgid, msg, language, mod_time=None):
        """Update a message in the translation service.

        If mod_time is None, then the current time should be inserted.
        """

    def deleteMessage(domain, msgid, language):
        """Delete a messahe in the translation service."""

    def addLanguage(language):
        """Add Language to Translation Service"""

    def addDomain(domain):
        """Add Domain to Translation Service"""

    def deleteLanguage(language):
        """Delete a Domain from the Translation Service."""

    def deleteDomain(domain):
        """Delete a Domain from the Translation Service."""


class ISyncTranslationService(Interface):
    """This interface allows translation services to be synchronized. The
       following four synchronization states can exist:

       0 - uptodate: The two messages are in sync.
                Default Action: Do nothing.

       1 - new: The message exists on the foreign TS, but is locally unknown.
                Default Action: Add the message to the local catalog.

       2 - older: The local version of the message is older than the one on
                the server.
                Default Action: Update the local message.

       3 - newer: The local version is newer than the foreign version.
                Default Action: Do nothing.

       4 - deleted: The message does not exist in the foreign TS.
                Default Action: Delete local version of message/
    """

    def getMessagesMapping(domains, languages, foreign_messages):
        """Creates a mapping of the passed foreign messages and the local ones.
        Returns a status report in a dictionary with keys of the form
        (msgid, domain, language) and values being a tuple of:

        foreign_mod_date, local_mod_date
        """

    def synchronize(messages_mapping):
        """Update the local message catalogs based on the foreign data.
        """


class ITranslationService(IReadTranslationService, IWriteTranslationService,
                          ISyncTranslationService):
    """This is the common and full-features translation service. Almost all
    translation service implementations will use this interface.

    An exception to this is the GlobalMessageCatalog as it will be read-only.
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


class IDomain(Interface):
    """A translation domain.

    Since it is often tedious to always specify a domain and a place for a
    particular translation, the idea of a Domain object was created, which
    allows to save the place and domain for a set of translations.

    Usage:

        domain = translationService.getDomain('domain')
        domain.translate('MyProductTitle', context)
    """

    def translate(msgid, mapping=None, context=None, target_language=None):
        """Translate the the source to its appropriate language.

        See ITranslationService for details.
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
        # which an adaptor is gotten for both the first arg and the second
        # arg.  I.e. getLanguage(obj, env)
        # But this isn't a good match for the iTranslationService.translate()
        # method. :(


class IUserPreferredCharsets(Interface):
    """This interface provides charset negotiation based on user preferences.
    """

    def getPreferredCharsets():
        """Return a sequence of user preferred charsets. Note that the order
           should describe the order of preference. Therefore the first
           character set in the list is the most preferred one.
        """
