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

$Id: Methods.py,v 1.1 2002/06/16 18:25:14 srichter Exp $
"""
from Zope.Proxy.ProxyIntrospection import removeAllProxies

from Zope.Publisher.XMLRPC.XMLRPCView import XMLRPCView
from Zope.App.PageTemplate import ViewPageTemplateFile


class Methods(XMLRPCView):

    __implements__ = XMLRPCView.__implements__
        
    def getAllDomains(self):
        return self.context.getAllDomains()


    def getAllLanguages(self):
        return self.context.getAllLanguages()


    def getMessagesFor(self, domains, languages):
        messages = []
        for domain in domains:
            for msg in self.context.getMessagesOfDomain(domain):
                if msg['language'] in languages:
                    messages.append(removeAllProxies(msg))

        return messages
