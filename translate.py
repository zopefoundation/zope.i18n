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
"""Translator

$Id: translate.py,v 1.9 2004/02/05 22:52:21 srichter Exp $
"""
from zope.i18n.interfaces import ITranslator
from zope.component import getService
from zope.interface import implements


class Translator:
    """A collaborative object which contains the domain, context, and locale.

    It is expected that object be constructed with enough information to find
    the domain, context, and target language.
    """

    implements(ITranslator)

    def __init__(self, locale, domain, context=None):
        """locale comes from the request, domain specifies the application,
        and context specifies the place (it may be none for global contexts).
        """
        self._locale = locale
        self._domain = domain
        self._context = context
        self._translation_service = getService(context, 'Translation')

    def translate(self, msgid, mapping=None, default=None):
        """Translate the source msgid using the given mapping.

        See ITranslationService for details.
        """
        # XXX Note that we cannot pass `context` to translation service as it
        #     is most likely a Zope container that is not adaptable to
        #     IUserPreferredLanguages.  It would be possible to pass the
        #     request if we had it (ZopeContext, which is currently the only
        #     user of Translator, has the request and could pass it to us
        #     here).
        #
        #     OTOH if the request had information about user's preferred
        #     languages, self._locale.id.language would most likely be not
        #     None.  Therefore passing request is only useful in one case:
        #     when the user asked for an exotic language for which we have no
        #     locale, and there were no fallback languages with a supported
        #     locale.
        #
        #     Note that this also uncovers an interesting situation.  Suppose
        #     the user sets HTTP_ACCEPT_LANGUAGES to lg, en;q=0.5.
        #     BrowserRequest looks for a locale matching 'lg', does not find
        #     it and settles on a locale for 'en'.  When we get here,
        #     self._locale.id.language is 'en', so 'lg' translations will not
        #     be used even if available.  Perhaps the fix would be to only
        #     specify context=self.request and just ignore
        #     self._locale.id.language.
        return self._translation_service.translate(
            msgid, self._domain, mapping=mapping,
            target_language=self._locale.id.language,
            default=default)
