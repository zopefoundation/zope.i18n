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
"""

$Id: IMessageCatalog.py,v 1.5 2002/06/16 18:25:13 srichter Exp $
"""

from Interface import Interface


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

        If the message id is not found, no exception is raised.  Instead
        default is returned, but if default is None, then msgid itself is
        returned.
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
