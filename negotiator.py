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

$Id: negotiator.py,v 1.7 2004/02/27 17:48:42 sidnei Exp $
"""

from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.component import getAdapter
from zope.interface import implements

def normalize_lang(lang):
    lang = lang.strip().lower()
    lang = lang.replace('_', '-')
    lang = lang.replace(' ', '')
    return lang

def normalize_langs(langs):
    # Make a mapping from normalized->original
    # so we keep can match the normalized lang
    # and return the original string.
    n_langs = {}
    for l in langs:
        n_langs[normalize_lang(l)] = l
    return n_langs

class Negotiator:

    implements(INegotiator)

    def getLanguage(self, langs, env):
        envadapter = getAdapter(env, IUserPreferredLanguages)
        userlangs = envadapter.getPreferredLanguages()
        # Prioritize on the user preferred languages.  Return the first user
        # preferred language that the object has available.
        langs = normalize_langs(langs)
        for lang in userlangs:
            if lang in langs:
                return langs.get(lang)
        return None


negotiator = Negotiator()
