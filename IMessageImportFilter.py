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
"""Translation Service Message Import Filter Interface

$Id: IMessageImportFilter.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""

from Interface import Interface

class IMessageImportFilter(Interface):
    """The Import Filter for Translation Service Messages.

       Classes implementing this interface should usually be Adaptors, as
       they adapt the IEditableTranslationService interface."""


    def importMessages(domains, languages, file):
        """Import all messages that are defined in the specified domains and
           languages.

           Note that some implementations might limit to only one domain and
           one language. A good example for that is a GettextFile.
        """
