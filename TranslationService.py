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

$Id: TranslationService.py,v 1.5 2002/06/12 20:59:09 bwarsaw Exp $
"""
import re
from types import StringTypes, TupleType

import Persistence
from Persistence.BTrees.OOBTree import OOBTree

from Zope.ComponentArchitecture import createObject
from Zope.ComponentArchitecture import getService

from Zope.App.OFS.Container.BTreeContainer import BTreeContainer
from Zope.App.OFS.Container.IContainer import IContainer
from Zope.App.OFS.Container.IContainer import IHomogenousContainer

from Zope.I18n.Negotiator import negotiator
from Zope.I18n.Domain import Domain
from Zope.I18n.IMessageCatalog import IMessageCatalog
from Zope.I18n.ITranslationService import ITranslationService
from Zope.I18n.SimpleTranslationService import SimpleTranslationService


class ILocalTranslationService(ITranslationService,
                               IContainer, IHomogenousContainer):
    """TTW manageable translation service"""


class TranslationService(BTreeContainer, SimpleTranslationService):

    __implements__ =  ILocalTranslationService

    def __init__(self, default_domain='global'):
        super(TranslationService, self).__init__()
        self._catalogs = OOBTree()
        self.default_domain = default_domain


    def _registerMessageCatalog(self, language, domain, catalog_name):
        if (language, domain) not in self._catalogs.keys():
            self._catalogs[(language, domain)] = []

        mc = self._catalogs[(language, domain)]
        mc.append(catalog_name)


    def _unregisterMessageCatalog(self, language, domain, catalog_name):
        self._catalogs[(language, domain)].remove(catalog_name)


    ############################################################
    # Implementation methods for interface
    # Zope.App.OFS.Container.IContainer.IWriteContainer

    def setObject(self, name, object):
        'See Zope.App.OFS.Container.IContainer.IWriteContainer'
        super(TranslationService, self).setObject(name, object)
        self._registerMessageCatalog(object.getLanguage(), object.getDomain(),
                                     name)
        return name

    def __delitem__(self, name):
        'See Zope.App.OFS.Container.IContainer.IWriteContainer'
        object = self[name]
        super(TranslationService, self).__delitem__(name)
        self._unregisterMessageCatalog(object.getLanguage(),
                                       object.getDomain(), name)

    def isAddable(self, interfaces):
        """See Zope.App.OFS.Container.IContainer.IWriteContainer"""
        if type(interfaces) != TupleType:
            interfaces = (interfaces,)
        if IMessageCatalog in interfaces:
            return 1
        return 0

    # end Zope.App.OFS.Container.IContainer.IWriteContainer
    ############################################################


    ############################################################
    # Implementation methods for interface
    # Zope.I18n.ITranslationService.

    def translate(self, domain, msgid, mapping=None, context=None,  
                  target_language=None):
        """See interface ITranslationService"""

        if domain is None:
            domain = self.default_domain

        if target_language is None:
            if context is None:
                raise TypeError, 'No destination language'
            else:
                avail_langs = self.getAvailableLanguages(domain)
                # Let's negotiate the language to translate to. :)
                negotiator = getService(self, 'LanguageNegotiation')
                target_language = negotiator.getLanguage(avail_langs, context)

        # Get the translation. Default is the source text itself.
        catalog_names = self._catalogs.get((target_language, domain), [])

        text = msgid
        for name in catalog_names:
            catalog = super(TranslationService, self).__getitem__(name)
            try:
                text = catalog.getMessage(msgid)
                break
            except:
                pass

        # Now we need to do the interpolation
        return self.interpolate(text, mapping)

    # end Zope.I18n.ITranslationService
    ############################################################


    def getMessageIdsOfDomain(self, domain, filter='%'):
        """Get all the message ids of a particular domain."""
        filter = filter.replace('%', '.*')
        filter_re = re.compile(filter)
        
        msgids = {}
        languages = self.getAvailableLanguages(domain)
        for language in languages:
            for name in self._catalogs[(language, domain)]:
                for msgid in self[name].getMessageIds():
                    if filter_re.match(msgid) >= 0:
                        msgids[msgid] = None
        return msgids.keys()


    def getAllLanguages(self):
        """Find all the languages that are available"""
        languages = {}
        for key in self._catalogs.keys():
            languages[key[0]] = None
        return languages.keys()


    def getAllDomains(self):
        """Find all available domains."""
        domains = {}
        for key in self._catalogs.keys():
            domains[key[1]] = None
        return domains.keys()


    def getAvailableLanguages(self, domain):
        """Find all the languages that are available for this domain"""
        identifiers = self._catalogs.keys()
        identifiers = filter(lambda x, d=domain: x[1] == d, identifiers)
        languages = map(lambda x: x[0], identifiers)
        return languages


    def getAvailableDomains(self, language):
        """Find all available domains."""
        identifiers = self._catalogs.keys()
        identifiers = filter(lambda x, l=language: x[0] == l, identifiers)
        domains = map(lambda x: x[1], identifiers)
        return domains
        

    def addMessage(self, domain, msg_id, msg, target_language):
        """ """
        catalog_name = self._catalogs[(target_language, domain)][0]
        catalog = self[catalog_name]
        catalog.setMessage(msg_id, msg)


    def updateMessage(self, domain, msg_id, msg, target_language):
        """ """
        catalog_name = self._catalogs[(target_language, domain)][0]
        catalog = self[catalog_name]
        catalog.setMessage(msg_id, msg)


    def deleteMessage(self, domain, msg_id, target_language):
        """ """
        catalog_name = self._catalogs[(target_language, domain)][0]
        catalog = self[catalog_name]
        catalog.deleteMessage(msg_id)


    def addLanguage(self, language):
        """Add Language to Translation Service"""
        domains = self.getAllDomains()
        if not domains:
            domains = [self.default_domain]

        for domain in domains:
            catalog = createObject(self, 'Message Catalog', language, domain)
            self.setObject('%s-%s' %(domain, language), catalog)


    def addDomain(self, domain):
        """Add Domain to Translation Service"""
        languages = self.getAllLanguages()
        if not languages:
            languages = ['en']

        for language in languages:
            catalog = createObject(self, 'Message Catalog', language, domain)
            self.setObject('%s-%s' %(domain, language), catalog)


    def deleteLanguage(self, language):
        """Delete a Domain from the Translation Service."""
        domains = self.getAvailableDomains(language)
        for domain in domains:
            for name in self._catalogs[(language, domain)]:
                if self.has_key(name):
                    del self[name]
            del self._catalogs[(language, domain)]

    def deleteDomain(self, domain):
        """Delete a Domain from the Translation Service."""
        languages = self.getAvailableLanguages(domain)
        for language in languages:
            for name in self._catalogs[(language, domain)]:
                if self.has_key(name):
                    del self[name]
            del self._catalogs[(language, domain)]


