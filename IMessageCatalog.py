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

$Id: IMessageCatalog.py,v 1.3 2002/06/12 15:54:01 bwarsaw Exp $
"""

from Interface import Interface


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
        """Return the language this message catalog is representing.
        """
        
    def getDomain():
        """Return the domain this message catalog is serving.
        """

    def getIdentifier():
        """Return an identifier for this message catalog.

        Note that this identifier does not have to be unique as several
        message catalogs could be serving the same domain and language.
        """
