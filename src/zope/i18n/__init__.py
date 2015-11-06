##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""
import sys
import re

from zope.component import queryUtility
from zope.i18nmessageid import MessageFactory, Message

from zope.i18n.config import ALLOWED_LANGUAGES
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IFallbackTranslationDomainFactory

from ._compat import _u

PY3 = sys.version_info[0] == 3
if PY3:
    unicode = str

# Set up regular expressions for finding interpolation variables in text.
# NAME_RE must exactly match the expression of the same name in the
# zope.tal.taldefs module:
NAME_RE = r"[a-zA-Z_][-a-zA-Z0-9_]*"

_interp_regex = re.compile(r'(?<!\$)(\$(?:(%(n)s)|{(%(n)s)}))'
    % ({'n': NAME_RE}))


def negotiate(context):
    """Negotiate language.

    This only works if the languages are set globally, otherwise each message
    catalog needs to do the language negotiation.
    """
    if ALLOWED_LANGUAGES is not None:
        negotiator = queryUtility(INegotiator)
        if negotiator is not None:
            return negotiator.getLanguage(ALLOWED_LANGUAGES, context)
    return None

def translate(msgid, domain=None, mapping=None, context=None,
               target_language=None, default=None):
    """Translate text.

    First setup some test components:

    >>> from zope import component, interface
    >>> import zope.i18n.interfaces

    >>> @interface.implementer(zope.i18n.interfaces.ITranslationDomain)
    ... class TestDomain:
    ...
    ...     def __init__(self, **catalog):
    ...         self.catalog = catalog
    ...
    ...     def translate(self, text, *_, **__):
    ...         return self.catalog[text]

    Normally, the translation system will use a domain utility:

    >>> component.provideUtility(TestDomain(eek=_u("ook")), name='my.domain')
    >>> translate(_u("eek"), 'my.domain')
    u'ook'

    Normally, if no domain is given, or if there is no domain utility
    for the given domain, then the text isn't translated:

    >>> translate(_u("eek"))
    u'eek'

    Moreover the text will be converted to unicode:

    >>> translate('eek', 'your.domain')
    u'eek'

    A fallback domain factory can be provided. This is normally used
    for testing:

    >>> def fallback(domain=_u("")):
    ...     return TestDomain(eek=_u("test-from-") + domain)
    >>> interface.directlyProvides(
    ...     fallback,
    ...     zope.i18n.interfaces.IFallbackTranslationDomainFactory,
    ...     )

    >>> component.provideUtility(fallback)

    >>> translate(_u("eek"))
    u'test-from-'

    >>> translate(_u("eek"), 'your.domain')
    u'test-from-your.domain'
    """

    if isinstance(msgid, Message):
        domain = msgid.domain
        default = msgid.default
        mapping = msgid.mapping

    if default is None:
        default = unicode(msgid)

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

    if target_language is None and context is not None:
        target_language = negotiate(context)

    return util.translate(msgid, mapping, context, target_language, default)

def interpolate(text, mapping=None):
    """Insert the data passed from mapping into the text.

    First setup a test mapping:

    >>> mapping = {"name": "Zope", "version": 3}

    In the text we can use substitution slots like $varname or ${varname}:

    >>> from zope.i18n._compat import _u
    >>> interpolate(_u("This is $name version ${version}."), mapping)
    u'This is Zope version 3.'

    Interpolation variables can be used more than once in the text:

    >>> interpolate(_u("This is $name version ${version}. ${name} $version!"),
    ...             mapping)
    u'This is Zope version 3. Zope 3!'

    In case if the variable wasn't found in the mapping or '$$' form
    was used no substitution will happens:

    >>> interpolate(_u("This is $name $version. $unknown $$name $${version}."),
    ...             mapping)
    u'This is Zope 3. $unknown $$name $${version}.'

    >>> interpolate(_u("This is ${name}"))
    u'This is ${name}'

    If a mapping value is a message id itself it is interpolated, too:

    >>> from zope.i18nmessageid import Message
    >>> interpolate(_u("This is $meta."),
    ...             mapping={'meta': Message(_u("$name $version"),
    ...                                      mapping=mapping)})
    u'This is Zope 3.'
    """

    def replace(match):
        whole, param1, param2 = match.groups()
        value = mapping.get(param1 or param2, whole)
        if isinstance(value, Message):
            value = interpolate(value, value.mapping)
        return unicode(value)

    if not text or not mapping:
        return text

    return _interp_regex.sub(replace, text)
