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

$Id: Translate.py,v 1.3 2002/07/01 22:50:06 bwarsaw Exp $
"""


def translate(place, domain, source, mapping=None, context=None,
              target_language=None):
    """Translates a source text based on a location in the Zope architecture
       and a domain."""

    # Lookup service...
    service = None

    return service.translate(domain, source, mapping, context, target_language)
