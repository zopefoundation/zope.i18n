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
"""Synchronize with Foreign Translation Services

$Id: BaseTranslationServiceView.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""

from Zope.Publisher.Browser.BrowserView import BrowserView
from Zope.I18n.ITranslationService import ITranslationService


class BaseTranslationServiceView(BrowserView):
    
    __used_for__ = ITranslationService


    def getAllLanguages(self):
        """Get all available languages from the Translation Service."""
        return self.context.getAllLanguages()


    def getAllDomains(self):
        return self.context.getAllDomains()
