##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Message IDs.


$Id: messageid.py,v 1.2 2003/04/03 17:25:15 jim Exp $
"""

class MessageID(unicode):
    """Message ID.

    This is a string used as a message ID. It has a domain attribute
    that is its source domain, and a default attribute that is its
    default text to display when there is no translation.
    
    """

    __slots__ = ('domain', 'default')

    def setDefault(self, default):
        self.default = default 

class MessageIDFactory:
    """Factory for creating MessageIDs.
    """
    
    def __init__(self, domain):
        self.domain = domain

    def __call__(self, ustr):
        result = MessageID(ustr)
        result.domain = self.domain
        result.default = None
        return result
    
