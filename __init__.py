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
"""i18n support.

$Id: __init__.py,v 1.5 2004/03/19 12:00:06 jim Exp $
"""
import re
from zope.i18nmessageid import MessageIDFactory, MessageID
from zope.i18n.interfaces import ITranslationDomain

# Set up regular expressions for finding interpolation variables in text.
# NAME_RE must exactly match the expression of the same name in the
# zope.tal.taldefs module:
NAME_RE = r"[a-zA-Z][-a-zA-Z0-9_]*"

_interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))
_get_var_regex = re.compile(r'%(n)s' %({'n': NAME_RE}))


def translate(location, msgid, domain=None, mapping=None, context=None,
              target_language=None, default=None):

    # XXX: For some reason, I get a recursive import when placing this import
    #      outside the function. I have no clue how to fix this. SR
    from zope.component import queryUtility

    if isinstance(msgid, MessageID):
        domain = msgid.domain
        default = msgid.default
        mapping = msgid.mapping

    util = queryUtility(location, ITranslationDomain, name=domain)

    if util is None:
        return interpolate(default, mapping)

    return util.translate(msgid, mapping, context, target_language, default)


def interpolate(text, mapping):
    """Insert the data passed from mapping into the text"""

    # If no translation was found, there is nothing to do.
    if text is None:
        return None

    # If the mapping does not exist, make a "raw translation" without
    # interpolation.
    if mapping is None:
        return text

    # Find all the spots we want to substitute
    to_replace = _interp_regex.findall(text)

    # Now substitute with the variables in mapping
    for string in to_replace:
        var = _get_var_regex.findall(string)[0]
        text = text.replace(string, unicode(mapping.get(var)))

    return text


              
