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

$Id: IDomain.py,v 1.4 2002/06/12 20:55:59 bwarsaw Exp $
"""

from Interface import Interface

class IDomain(Interface):
    """A translation domain.

    Since it is often tedious to always specify a domain and a place for a
    particular translation, the idea of a Domain object was created, which
    allows to save the place and domain for a set of translations.

    Usage:

        domain = translationService.getDomain('domain')
        domain.translate('MyProductTitle', context)
    """

    def translate(msgid, mapping=None, context=None, target_language=None):
        """Translate the the source to its appropriate language.

        See ITranslationService for details.
        """
