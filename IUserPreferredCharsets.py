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
"""See IUserPreferredCharsets.

$Id: IUserPreferredCharsets.py,v 1.1 2002/06/14 08:56:29 srichter Exp $
"""

from Interface import Interface

class IUserPreferredCharsets(Interface):
    """This interface provides charset negotiation based on user preferences.
    """
  
    def getPreferredCharsets():
        """Return a sequence of user preferred charsets. Note that the order
           should describe the order of preference. Therefore the first
           character set in the list is the most preferred one.
        """
