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

$Id: IUserPreferredLanguages.py,v 1.1 2002/06/12 15:56:18 bwarsaw Exp $
"""

from Interface import Interface

class IUserPreferredLanguages(Interface):

    """This interface provides language negotiation based on user preferences.
    """
  
    def getPreferredLanguages():
        """Return a sequence of user preferred languages.
        """
