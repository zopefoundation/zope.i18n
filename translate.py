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

$Id: translate.py,v 1.4 2003/04/03 19:55:20 fdrake Exp $
"""

from zope.i18n.interfaces import ITranslator
from zope.component import getService


class Translator:
    """A collaborative object which contains the domain, context, and locale.

    It is expected that object be constructed with enough information to find
    the domain, context, and target language.
    """

    __implements__ = ITranslator

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
        return self._translation_service.translate(
            self._domain, msgid, mapping, self._context,
            self._locale.id.language,
            default=default)
