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

$Id: MessageCatalog.py,v 1.5 2002/06/13 13:13:07 srichter Exp $
"""

from Persistence.BTrees.OOBTree import OOBTree
from Persistence import Persistent
from Zope.ComponentArchitecture.IFactory import IFactory
from Zope.App.Security.RegisteredObject import RegisteredObject
from Zope.I18n.IMessageCatalog import IMessageCatalog


class MessageCatalog(RegisteredObject, Persistent):

    __implements__ =  IMessageCatalog
    __class_implements__ = IFactory

    def __init__(self, language, domain="default"):
        """Initialize the message catalog"""
        super(MessageCatalog, self).__init__('', '', '')
        self._language = language
        self._domain = domain
        self._messages = OOBTree()
    
    def setMessage(self, msgid, message):
        """Set a message to the catalog."""
        self._messages[msgid] = message

    def deleteMessage(self, msgid):
        """Set a message to the catalog."""
        del self._messages[msgid]

    def getMessageIds(self):
        """Get a list of all the message ids."""
        return list(self._messages.keys())
        

    ############################################################
    # Implementation methods for interface
    # Zope/ComponentArchitecture/IFactory.py

    def getInterfaces(self):
        'See Zope.ComponentArchitecture.IFactory.IFactory'
        return self.__implements__
        
    #
    ############################################################

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
