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

$Id: MessageCatalog.py,v 1.7 2002/06/20 15:55:07 jim Exp $
"""
import time

from Persistence.BTrees.OOBTree import OOBTree
from Persistence import Persistent
from Zope.Proxy.ProxyIntrospection import removeAllProxies
from Zope.ComponentArchitecture.IFactory import IFactory
from Zope.App.Security.Registries.RegisteredObject import RegisteredObject
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
    

    ############################################################
    # Implementation methods for interface
    # Zope.I18n.IMessageCatalog.IMessageCatalog

    ######################################
    # from: Zope.I18n.IMessageCatalog.IReadMessageCatalog

    def getMessage(self, id):
        'See Zope.I18n.IMessageCatalog.IReadMessageCatalog'
        return removeAllProxies(self._messages[id][0])

    def queryMessage(self, id, default=None):
        'See Zope.I18n.IMessageCatalog.IReadMessageCatalog'
        if default is None:
            default = id
        result = removeAllProxies(self._messages.get(id, default))
        if result != default: result = result[0]
        return result

    def getLanguage(self):
        'See Zope.I18n.IMessageCatalog.IReadMessageCatalog'
        return self._language
        
    def getDomain(self):
        'See Zope.I18n.IMessageCatalog.IReadMessageCatalog'
        return self._domain

    def getIdentifier(self):
        'See Zope.I18n.IMessageCatalog.IReadMessageCatalog'
        return (self._language, self._domain)
        
    ######################################
    # from: Zope.I18n.IMessageCatalog.IWriteMessageCatalog

    def getFullMessage(self, msgid):
        'See Zope.I18n.IMessageCatalog.IWriteMessageCatalog'
        message = removeAllProxies(self._messages[msgid])
        return {'domain'   : self._domain,
                'language' : self._language,
                'msgid'    : msgid,
                'msgstr'   : message[0],
                'mod_time' : message[1]}

    def setMessage(self, msgid, message, mod_time=None):
        'See Zope.I18n.IMessageCatalog.IWriteMessageCatalog'
        if mod_time is None:
            mod_time = int(time.time())
        self._messages[msgid] = (message, mod_time)
        
    def deleteMessage(self, msgid):
        'See Zope.I18n.IMessageCatalog.IWriteMessageCatalog'
        del self._messages[msgid]

    def getMessageIds(self):
        'See Zope.I18n.IMessageCatalog.IWriteMessageCatalog'
        return list(self._messages.keys())

    def getMessages(self):
        'See Zope.I18n.IMessageCatalog.IWriteMessageCatalog'
        messages = []
        for message in self._messages.items():
            messages.append({'domain'   : self._domain,
                             'language' : self._language,
                             'msgid'    : message[0],
                             'msgstr'   : message[1][0],
                             'mod_time' : message[1][1]})
        return messages

    #
    ############################################################

    ############################################################
    # Implementation methods for interface
    # Zope/ComponentArchitecture/IFactory.py

    def getInterfaces(self):
        'See Zope.ComponentArchitecture.IFactory.IFactory'
        return self.__implements__
        
    #
    ############################################################
