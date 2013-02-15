##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""A simple implementation of a Message Catalog.
"""
import sys
from gettext import GNUTranslations
from zope.i18n.interfaces import IGlobalMessageCatalog
from zope.interface import implementer

PY2 = sys.version_info[0] == 2

class _KeyErrorRaisingFallback(object):
    def ugettext(self, message):
        raise KeyError(message)
    gettext = ugettext


@implementer(IGlobalMessageCatalog)
class GettextMessageCatalog(object):
    """A message catalog based on GNU gettext and Python's gettext module."""

    def __init__(self, language, domain, path_to_file):
        """Initialize the message catalog"""
        self.language = language
        self.domain = domain
        self._path_to_file = path_to_file
        self.reload()
        self._catalog.add_fallback(_KeyErrorRaisingFallback())
        if PY2:
            self._gettext = self._catalog.ugettext
        else:
            self._gettext = self._catalog.gettext

    def reload(self):
        'See IMessageCatalog'
        fp = open(self._path_to_file, 'rb')
        try:
            self._catalog = GNUTranslations(fp)
        finally:
            fp.close()

    def getMessage(self, id):
        'See IMessageCatalog'
        return self._gettext(id)

    def queryMessage(self, id, default=None):
        'See IMessageCatalog'
        try:
            return self._gettext(id)
        except KeyError:
            return default

    def getIdentifier(self):
        'See IMessageCatalog'
        return self._path_to_file
