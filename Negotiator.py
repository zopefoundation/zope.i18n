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

$Id: Negotiator.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""

from Zope.I18n.INegotiator import INegotiator
from Zope.I18n.IUserPreferedLanguages import IUserPreferedLanguages
from Zope.ComponentArchitecture import getAdapter

class Negotiator:

    __implements__ = INegotiator

    def getLanguage(self, object_langs, env):

        adapter  = getAdapter(env, IUserPreferedLanguages)
        user_langs = adapter.getLanguages()

        for lang in user_langs:
            if lang in object_langs:
                return lang

        return None


negotiator = Negotiator()
