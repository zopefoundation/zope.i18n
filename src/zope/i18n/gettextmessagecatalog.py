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

from gettext import GNUTranslations
from zope.i18n.interfaces import IGlobalMessageCatalog
from zope.interface import implementer


class _KeyErrorRaisingFallback(object):
    def ugettext(self, message):
        raise KeyError(message)
    gettext = ugettext


@implementer(IGlobalMessageCatalog)
class GettextMessageCatalog(object):
    """A message catalog based on GNU gettext and Python's gettext module."""

    _catalog = None

    def __init__(self, language, domain, path_to_file):
        """Initialize the message catalog"""
        self.language = language.decode('utf-8') if isinstance(language, bytes) else language
        self.domain = domain.decode("utf-8") if isinstance(domain, bytes) else domain
        self._path_to_file = path_to_file
        self.reload()
        catalog = self._catalog
        catalog.add_fallback(_KeyErrorRaisingFallback())
        self._gettext = catalog.gettext if str is not bytes else catalog.ugettext

    def reload(self):
        'See IMessageCatalog'
        with open(self._path_to_file, 'rb') as fp:
            self._catalog = GNUTranslations(fp)

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
