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
"""Translation Service Message Export Filter Interface

$Id: IMessageExportFilter.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""

from Interface import Interface

class IMessageExportFilter(Interface):
    """The Export Filter for Translation Service Messages.

       Classes implementing this interface should usually be Adaptors, as
       they adapt the IEditableTranslationService interface."""


    def exportMessages(domains, languages):
        """Export all messages that are defined in the specified domains and
           languages.

           Note that some implementations might limit to only one domain and
           one language. A good example for that is a GettextFile.
        """
