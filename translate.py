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
"""Translator

$Id: translate.py,v 1.10 2004/02/27 22:25:22 srichter Exp $
"""
from zope.i18n.interfaces import ITranslator
from zope.component import getService
from zope.interface import implements


class Translator:
    """A collaborative object which contains the domain, context, and locale.

    It is expected that object be constructed with enough information to find
    the domain, context, and target language.
    """
    implements(ITranslator)

    def __init__(self, domain, context, location=None):
        """Initialize the object."""
        self._domain = domain
        self._context = context
        self._translation_service = getService(location, 'Translation')


    def translate(self, msgid, mapping=None, default=None):
        """See zope.i18n.interfaces.ITranslator."""

        return self._translation_service.translate(
            msgid, self._domain, mapping=mapping, context=self._context,
            default=default)
