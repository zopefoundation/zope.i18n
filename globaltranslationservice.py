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

$Id: globaltranslationservice.py,v 1.9 2003/04/17 20:05:13 bwarsaw Exp $
"""

from zope.i18n.negotiator import negotiator
from zope.i18n.simpletranslationservice import SimpleTranslationService
from zope.i18n.messageid import MessageID

# The configure.zcml file should specify a list of fallback languages for the
# site.  If a particular catalog for a negotiated language is not available,
# then the zcml specified order should be tried.  If that fails, then as a
# last resort the languages in the following list are tried.  If these fail
# too, then the msgid is returned.
#
# Note that these fallbacks are used only to find a catalog.  If a particular
# message in a catalog is not translated, tough luck, you get the msgid.
LANGUAGE_FALLBACKS = ['en']


class GlobalTranslationService(SimpleTranslationService):

    __implements__ =  SimpleTranslationService.__implements__

    def __init__(self, default_domain='global', fallbacks=None):
        # XXX We haven't specified that ITranslationServices have a default
        # domain.  So far, we've required the domain argument to .translate()
        self._domain = default_domain
        # _catalogs maps (language, domain) to IMessageCatalog instances
        self._catalogs = {}
        # _data maps IMessageCatalog.getIdentifier() to IMessageCatalog
        self._data = {}
        # What languages to fallback to, if there is no catalog for the
        # requested language (no fallback on individual messages)
        if fallbacks is None:
            fallbacks = LANGUAGE_FALLBACKS
        self._fallbacks = fallbacks

    def _registerMessageCatalog(self, language, domain, catalog_name):
        key = (language, domain)
        mc = self._catalogs.setdefault(key, [])
        mc.append(catalog_name)

    def addCatalog(self, catalog):
        self._data[catalog.getIdentifier()] = catalog
        self._registerMessageCatalog(catalog.getLanguage(),
                                     catalog.getDomain(),
                                     catalog.getIdentifier())

    def setLanguageFallbacks(self, fallbacks=None):
        if fallbacks is None:
            fallbacks = LANGUAGE_FALLBACKS
        self._fallbacks = fallbacks

    def translate(self, msgid, domain=None, mapping=None, context=None,
                  target_language=None, default=None):
        '''See interface ITranslationService'''
        if target_language is None and context is not None:
            # Try to determine target language from context
            langs = [m[0] for m in self._catalogs.keys()]
            target_language = negotiator.getLanguage(langs, context)

        # MessageID attributes override arguments
        if isinstance(msgid, MessageID):
            domain = msgid.domain
            mapping = msgid.mapping
            default = msgid.default

        # Get the translation. Use the specified fallbacks if this fails
        catalog_names = self._catalogs.get((target_language, domain))
        if catalog_names is None:
            for language in self._fallbacks:
                catalog_names = self._catalogs.get((language, domain))
                if catalog_names is not None:
                    break

        # Did the fallback fail?  Sigh, return None
        text = default
        if catalog_names:
            for name in catalog_names:
                catalog = self._data[name]
                s = catalog.queryMessage(msgid)
                if s is not None:
                    text = s
                    break

        # Now we need to do the interpolation
        if text is not None:
            text = self.interpolate(text, mapping)
        return text

translationService = GlobalTranslationService()


# Register our cleanup with Testing.CleanUp to make writing unit tests simpler.
from zope.testing.cleanup import addCleanUp
addCleanUp(translationService.__init__)
del addCleanUp
