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

$Id: messageid.py,v 1.4 2003/04/15 21:17:48 bwarsaw Exp $
"""

class MessageID(unicode):
    """Message ID.

    This is a string used as a message ID.  It has a domain attribute that is
    its source domain, and a default attribute that is its default text to
    display when there is no translation.  domain may be None meaning there is
    no translation domain.  default may also be None, in which case the
    message id itself implicitly serves as the default text.

    MessageID objects also have a mapping attribute which must be set after
    construction of the object.  This is used when translating and
    substituting variables.
    """

    __slots__ = ('domain', 'default', 'mapping')

    def __new__(cls, ustr, domain=None, default=None):
        self = unicode.__new__(cls, ustr)
        self.domain = domain
        if default is None:
            self.default = ustr
        else:
            self.default = default
        self.mapping = {}
        return self


class MessageIDFactory:
    """Factory for creating MessageIDs."""

    def __init__(self, domain):
        self._domain = domain

    def __call__(self, ustr):
        return MessageID(ustr, domain=self._domain)