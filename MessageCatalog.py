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
"""A simple implementation of a Message Catalog. 

$Id: MessageCatalog.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""

from Zope.I18n.IMessageCatalog import IMessageCatalog


class MessageCatalog:

    __implements__ =  IMessageCatalog


    def __init__(self, language, domain="global"):
        """Initialize the message catalog"""
        self._language = language
        self._domain = domain
        self._messages = {}
    

    def setMessage(self, id, message):
        """Set a message to the catalog."""
        self._messages[id] = message
        

    ############################################################
    # Implementation methods for interface
    # Zope.I18n.IMessageCatalog.

    def getMessage(self, id):
        'See Zope.I18n.IMessageCatalog.IMessageCatalog'
        return self._messages[id]

    def queryMessage(self, id, default=None):
        'See Zope.I18n.IMessageCatalog.IMessageCatalog'
        if default is None:
            default = id
        return self._messages.get(id, default)

    def getLanguage(self):
        'See Zope.I18n.IMessageCatalog.IMessageCatalog'
        return self._language
        
    def getDomain(self):
        'See Zope.I18n.IMessageCatalog.IMessageCatalog'
        return self._domain

    def getIdentifier(self):
        'See Zope.I18n.IMessageCatalog.IMessageCatalog'
        return (self._language, self._domain)
        
    #
    ############################################################
