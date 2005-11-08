##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test message catalog

$Id$
"""

from zope import interface
from zope.i18n.interfaces import IGlobalMessageCatalog

class TestMessageCatalog:
    interface.implements(IGlobalMessageCatalog)

    language = 'test'

    def __init__(self, domain):
        self.domain = domain

    def queryMessage(self, msgid, default=None):
        return u'[[%s][%s]]' % (self.domain or getattr(msgid, 'domain', ''),
                                msgid)

    getMessage = queryMessage

    def getIdentifier(self):
        return 'test'

    def reload(self):
        pass

                     
