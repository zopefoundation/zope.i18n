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
"""Translation Service related Interfaces.

$Id: ITranslationService.py,v 1.4 2002/06/16 18:25:13 srichter Exp $
"""

from Interface import Interface


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
        Retruns a status report in a dictionary with keys of the form
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
