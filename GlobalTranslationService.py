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

$Id: GlobalTranslationService.py,v 1.4 2002/06/13 16:35:19 srichter Exp $
"""

from Negotiator import negotiator
from SimpleTranslationService import SimpleTranslationService


class GlobalTranslationService(SimpleTranslationService):

    __implements__ =  SimpleTranslationService.__implements__

    def __init__(self, default_domain='global'):
        # XXX We haven't specified that ITranslationServices have a default
        # domain.  So far, we've required the domain argument to .translate()
        self._domain = default_domain
        # _catalogs maps (language, domain) to IMessageCatalog instances
        self._catalogs = {}
        # _data maps IMessageCatalog.getIdentifier() to IMessageCatalog
        self._data = {}

    def _registerMessageCatalog(self, language, domain, catalog_name):
        key = (language, domain)
        mc = self._catalogs.setdefault(key, [])
        mc.append(catalog_name)

    def addCatalog(self, catalog):
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
        if target_language is None:
            if context is None:
                raise TypeError, 'No destination language'
            else:
                langs = [m[0] for m in self._catalogs.keys()]
                target_language = negotiator.getLanguage(langs, context)

        # Get the translation. Default is the msgid text itself.
        catalog_names = self._catalogs.get((target_language, domain), [])

        text = msgid
        for name in catalog_names:
            catalog = self._data[name]
            text = catalog.queryMessage(msgid)

        # Now we need to do the interpolation
        return self.interpolate(text, mapping)

    #
    ############################################################


translationService = GlobalTranslationService()
