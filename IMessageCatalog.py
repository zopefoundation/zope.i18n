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

$Id: IMessageCatalog.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""

from Interface import Interface


class IMessageCatalog(Interface):
    """Translation Service

    This interface provides a method for translating a message or message id,
    including text with interpolation. The message catalog basically serves as
    a fairly simple mapping object.

    A single Message Catalog represents a particular language and
    domain. Therefore you will have the following constructor arguments:

    language -- The language of the returning language. This is a read-only
                attribute.

    domain -- The translation domain for this messages. This is a read-only
              attribute. See ITranslationService.

    When we refer to text here, we mean text that follows the standard
    Zope 3 text representation.
    """

    def getMessage(id):
        """Return the appropriate text for the given id. As all get methods,
           this will raise an error, if the id is not found
        """

    def queryMessage(id, default=None):
        """Return the appropriate test for the given id, but if the id is not
           found, it should not raise an error, instead returning default. If
           default is None, then the id itself is returned.
        """
        
    def getLanguage():
        """Return the langauge this message catalog is representing.
        """
        
    def getDomain():
        """Return the domain this message catalog is serving.
        """

    def getIdentifier():
        """Return a identifier for this message catalog. Note that this
           identifier does not have to be unique as several message catalog
           could serve the same domain and language.
        """
