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
"""Global Translation Service for providing I18n to file-based code.

$Id: GlobalTranslationService.py,v 1.1 2002/06/12 18:38:56 srichter Exp $
"""

from Negotiator import negotiator
from SimpleTranslationService import SimpleTranslationService


class GlobalTranslationService(SimpleTranslationService):
    ''' '''

    __implements__ =  SimpleTranslationService.__implements__


    def __init__(self, default_domain='global'):
        ''' '''
        self._catalogs = {}
        self._data = {}


    def _registerMessageCatalog(self, language, domain, catalog_name):
        ''' '''
        if (language, domain) not in self._catalogs.keys():
            self._catalogs[(language, domain)] = []

        mc = self._catalogs[(language, domain)]
        mc.append(catalog_name)


    def addCatalog(self, catalog):
        ''' '''
        self._data[catalog.getIdentifier()] = catalog
        self._registerMessageCatalog(catalog.getLanguage(),
                                     catalog.getDomain(),
                                     catalog.getIdentifier())


    ############################################################
    # Implementation methods for interface
    # Zope.I18n.ITranslationService.

    def translate(self, domain, msgid, mapping=None, context=None,  
                  target_language=None):
        '''See interface ITranslationService'''

        if domain is None:
            domain = self.default_domain

        if target_language is None:
            if context is None:
                raise TypeError, 'No destination language'
            else:
                avail_langs = {}
                for catalog in self._data.values():
                    avail_langs[catalog] = None

                target_language = negotiator.getLanguage(avail_langs.keys(),
                                                         context)

        # Get the translation. Default is the msgid text itself.
        catalog_names = self._catalogs.get((target_language, domain), [])

        text = msgid
        for name in catalog_names:
            catalog = self._data[name]
            try:
                text = catalog.getMessage(msgid)
                break
            except:
                pass

        # Now we need to do the interpolation
        return self.interpolate(text, mapping)

    #
    ############################################################


translationService = GlobalTranslationService()
