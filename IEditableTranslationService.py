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
"""These methods are required for any TranslationService that will be
available for editing via Views; the prime example is the Browser of course.

$Id: IEditableTranslationService.py,v 1.1 2002/06/13 14:04:58 srichter Exp $
"""

from Interface import Interface


class IEditableTranslationService(Interface):
    """This interface describes the methods that are necessary for an editable
       Translation Service to work.
    """
    
    def getMessageIdsOfDomain(domain, filter='%'):
        """Get all the message ids of a particular domain."""

    def getAllLanguages():
        """Find all the languages that are available"""

    def getAllDomains():
        """Find all available domains."""

    def getAvailableLanguages(domain):
        """Find all the languages that are available for this domain"""

    def getAvailableDomains(language):
        """Find all available domains."""
        
    def addMessage(domain, msg_id, msg, target_language):
        """Add a message to the translation service."""

    def updateMessage(domain, msg_id, msg, target_language):
        """Update a message in the translation service."""

    def deleteMessage(domain, msg_id, target_language):
        """Delete a messahe in the translation service."""
        
    def addLanguage(language):
        """Add Language to Translation Service"""

    def addDomain(domain):
        """Add Domain to Translation Service"""

    def deleteLanguage(language):
        """Delete a Domain from the Translation Service."""

    def deleteDomain(domain):
        """Delete a Domain from the Translation Service."""


