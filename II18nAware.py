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
"""Internationalization of content objects.

$Id: II18nAware.py,v 1.1 2002/06/24 15:42:42 mgedmin Exp $
"""

from Interface import Interface


class II18nAware(Interface):
    """Internationalization aware content object.
    """

    def getDefaultLanguage():
    	"""Return the default language."""

    def setDefaultLanguage(language):
	"""Set the default language, which will be used if the language is not
	specified, or not available.
	"""
    
    def getAvailableLanguages():
        """Find all the languages that are available."""

