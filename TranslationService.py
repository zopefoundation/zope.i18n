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

$Id: TranslationService.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""
import re
from types import StringTypes, TupleType

import Persistence
from Persistence.BTrees.OOBTree import OOBTree

from Zope.App.OFS.Container.BTreeContainer import BTreeContainer
from Zope.App.OFS.Container.IContainer import IContainer
from Zope.App.OFS.Container.IContainer import IHomogenousContainer

from Negotiator import negotiator
from IMessageCatalog import IMessageCatalog
from ITranslationService import ITranslationService


# Setting up some regular expressions for finding interpolation variables in
# the text.
NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
_interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))
_get_var_regex = re.compile(r'%(n)s' %({'n': NAME_RE}))


class ILocalTranslationService(ITranslationService,
                               IContainer, IHomogenousContainer):
    """TTW manageable translation service"""


class TranslationService(BTreeContainer):
    ''' '''

    __implements__ =  ILocalTranslationService


    def __init__(self, default_domain='global'):
        ''' '''
        self.__data = OOBTree()
        self._catalogs = OOBTree()


    def _registerMessageCatalog(self, language, domain, catalog_name):
        ''' '''
        if (language, domain) not in self._catalogs.keys():
            self._catalogs[(language, domain)] = []

        mc = self._catalogs[(language, domain)]
        mc.append(catalog_name)


    def _unregisterMessageCatalog(self, language, domain, catalog_name):
        ''' '''
        mc = self._catalogs.get((language, domain), [])
        mc.append(catalog_name)


    ############################################################
    # Implementation methods for interface
    # Zope.App.OFS.Container.IContainer.IWriteContainer

    def setObject(self, name, object):
        'See Zope.App.OFS.Container.IContainer.IWriteContainer'
        if type(name) in StringTypes and len(name)==0:
            raise ValueError
        if not self.isAddable(getattr(object,'__implements__', None)):
            raise UnaddableError (self, object, name)
        self.__data[name] = object
        self._registerMessageCatalog(object.getLanguage(), object.getDomain(),
                                     name)
        return name

    def __delitem__(self, name):
        'See Zope.App.OFS.Container.IContainer.IWriteContainer'
        del self.__data[name]
        self._unregisterMessageCatalog(object.language, object.domain, name)
        

    def isAddable(self, interfaces):
        'See Zope.App.OFS.Container.IContainer.IWriteContainer'
        if type(interfaces) != TupleType:
            interfaces = (interfaces,)
        if IMessageCatalog in interfaces:
            return 1
        return 0

    #
    ############################################################


    ############################################################
    # Implementation methods for interface
    # Zope.I18n.ITranslationService.

    def translate(self, domain, source, mapping=None, context=None,  
                  target_language=None):
        '''See interface ITranslationService'''

        if domain is None:
            domain = self.default_domain

        if target_language is None:
            if context is None:
                raise TypeError, 'No destination language'
            else:
                avail_langs = self.getAvailableLanguages(domain)
                target_language = negotiator.getLanguage(avail_langs, context)

        # Get the translation. Default is the source text itself.
        catalog_names = self._catalogs.get((target_language, domain), {})

        text = source
        for name in catalog_names:
            catalog = self.__data[name]
            try:
                text = catalog.getMessage(source)
                break
            except:
                pass

        # Now we need to do the interpolation
        return self.interpolate(text, mapping)

    #
    ############################################################


    def interpolate(self, text, mapping):
        """Insert the data passed from mapping into the text"""

        to_replace = _interp_regex.findall(text)

        for string in to_replace:
            var = _get_var_regex.findall(string)[0]
            text = text.replace(string, mapping.get(var))

        return text


    def getAvailableLanguages(self, domain):
        """Find all the languages that are available for this domain"""
        identifiers = self._catalogs.keys()
        identifiers = filter(lambda x, d=domain: x[1] == domain, identifiers)
        languages = map(lambda x: x[0], identifiers)
        return languages
