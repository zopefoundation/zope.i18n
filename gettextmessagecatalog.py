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
"""A simple implementation of a Message Catalog.

$Id: gettextmessagecatalog.py,v 1.4 2003/03/25 23:25:14 bwarsaw Exp $
"""

from gettext import GNUTranslations
from zope.i18n.interfaces import IMessageCatalog


class GettextMessageCatalog:
    """ """

    __implements__ =  IMessageCatalog


    def __init__(self, language, domain, path_to_file):
        """Initialize the message catalog"""
        self._language = language
        self._domain = domain
        self._path_to_file = path_to_file
        self.__translation_object = None
        self._prepareTranslations()


    def _prepareTranslations(self):
        """ """
        if self.__translation_object is None:
            file = open(self._path_to_file, 'r')
            self.__translation_object = GNUTranslations(file)
            file.close()


    def getMessage(self, id):
        'See IMessageCatalog'
        self._prepareTranslations()
        msg = self.__translation_object.ugettext(id)
        if msg == id:
            raise KeyError
        return msg

    def queryMessage(self, id, default=None):
        'See IMessageCatalog'
        self._prepareTranslations()
        text = self.__translation_object.ugettext(id)
        if text != id:
            return text
        return default

    def getLanguage(self):
        'See IMessageCatalog'
        return self._language

    def getDomain(self):
        'See IMessageCatalog'
        return self._domain

    def getIdentifier(self):
        'See IMessageCatalog'
        return self._path_to_file
