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

$Id: IDomain.py,v 1.2 2002/06/10 23:29:27 jim Exp $
"""

from Interface import Interface

class IDomain(Interface):
    """Since it is often tedious to always specify a domain and place for a
       particular translation, the idea of a Domain object was created, which
       allows to save the place and domain for a set of translations.

       Usage:

       domain = Domain(self, 'MyProduct')
       domain.translate('MyProductTitle', context)

       Constructor Arguments:

         place -- A location where the Domain should look for the translation
                  service.

         domain -- Secifies the domain to look up for the translation. See
                   ITranslationService for more details on domains.
    """


    def translate(msgid, mapping=None, context=None, target_language=None):
        """Translate the the source to its appropriate language.

        See ITranslationService for details.
        """
