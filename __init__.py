##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""i18n support.

$Id$
"""
import re
import warnings

# BBB 2005/10/10 -- MessageIDs are to be removed for Zope 3.3
import zope.deprecation
zope.deprecation.__show__.off()
from zope.i18nmessageid import MessageIDFactory, MessageID
zope.deprecation.__show__.on()

from zope.i18nmessageid import MessageFactory, Message
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IFallbackTranslationDomainFactory
from zope.component import queryUtility


# Set up regular expressions for finding interpolation variables in text.
# NAME_RE must exactly match the expression of the same name in the
# zope.tal.taldefs module:
NAME_RE = r"[a-zA-Z][-a-zA-Z0-9_]*"

_interp_regex = re.compile(r'(?<!\$)(\$(?:(%(n)s)|{(%(n)s)}))'
    % ({'n': NAME_RE}))

def _translate(msgid, domain=None, mapping=None, context=None,
               target_language=None, default=None):

    if isinstance(msgid, (MessageID, Message)):
        domain = msgid.domain
        default = msgid.default
        mapping = msgid.mapping

    if default is None:
        default = msgid

    if domain:
        util = queryUtility(ITranslationDomain, domain)
        if util is None:
            util = queryUtility(IFallbackTranslationDomainFactory)
            if util is not None:
                util = util(domain)
    else:
        util = queryUtility(IFallbackTranslationDomainFactory)
        if util is not None:
            util = util()

    if util is None:
        return interpolate(default, mapping)

    return util.translate(msgid, mapping, context, target_language, default)

# BBB Backward compat
def translate(*args, **kw):
    if args and not isinstance(args[0], basestring):
        warnings.warn(
            "translate no longer takes a location argument. "
            "The argument was ignored.",
            DeprecationWarning, 2)
        args = args[1:]
    return _translate(*args, **kw)

def interpolate(text, mapping=None):
    """Insert the data passed from mapping into the text.

    First setup a test mapping:

    >>> mapping = {"name": "Zope", "version": 3}

    In the text we can use substitution slots like $varname or ${varname}:

    >>> interpolate(u"This is $name version ${version}.", mapping)
    u'This is Zope version 3.'

    Interpolation variables can be used more than once in the text:

    >>> interpolate(u"This is $name version ${version}. ${name} $version!",
    ...             mapping)
    u'This is Zope version 3. Zope 3!'

    In case if the variable wasn't found in the mapping or '$$' form
    was used no substitution will happens:

    >>> interpolate(u"This is $name $version. $unknown $$name $${version}.",
    ...             mapping)
    u'This is Zope 3. $unknown $$name $${version}.'

    >>> interpolate(u"This is ${name}")
    u'This is ${name}'
    """

    def replace(match):
        whole, param1, param2 = match.groups()
        return unicode(mapping.get(param1 or param2, whole))

    if not text or not mapping:
        return text

    return _interp_regex.sub(replace, text)
