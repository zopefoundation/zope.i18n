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
"""This is a simple implementation of the ITranslationService interface.

$Id: SimpleTranslationService.py,v 1.1 2002/06/12 18:38:56 srichter Exp $
"""

import re
from types import DictType
from Zope.ComponentArchitecture import getService
from ITranslationService import ITranslationService
from Domain import Domain


# Setting up some regular expressions for finding interpolation variables in
# the text.
NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
_interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))
_get_var_regex = re.compile(r'%(n)s' %({'n': NAME_RE}))


class SimpleTranslationService:
    """This is the simplest implementation of the ITranslationInterface I
       could come up with.

       The constructor takes one optional argument 'messages', which will be
       used to do the translation. The 'messages' attribute has to have the
       following structure:

       {('domain', 'language', 'msg_id'): 'message', ...}

       Note: This Translation Service does not implemen
    """

    __implements__ =  ITranslationService


    def __init__(self, messages=None):
        """Initializes the object. No arguments are needed."""
        if messages is None:
            self.messages = {}
        else:
            assert type(messages) == DictType
            self.messages = messages


    ############################################################
    # Implementation methods for interface
    # Zope.I18n.ITranslationService.

    def translate(self, domain, msgid, mapping=None, context=None,  
                  target_language=None):
        '''See interface ITranslationService'''

        # Find out what the target language should be
        if target_language is None:
            if context is None:
                raise TypeError, 'No destination language'
            else:
                avail_langs = map(lambda m: m[2], self.messages.keys())
                # Let's negotiate the language to translate to. :)
                negotiator = getService(self, 'LanguageNegotiation')
                target_language = negotiator.getLanguage(avail_langs, context)

        # Make a raw translation without interpolation
        text = self.messages.get((domain, target_language, msgid), msgid)

        # Now we need to do the interpolation
        return self.interpolate(text, mapping)


    def getDomain(self, domain):
        '''See interface ITranslationService'''
        return Domain(self, domain)

    #
    ############################################################


    def interpolate(self, text, mapping):
        """Insert the data passed from mapping into the text"""

        # If the mapping does not exist, make a "raw translation" without
        # interpolation. 
        if mapping is None:
            return text

        # Find all the spots we want to substitute
        to_replace = _interp_regex.findall(text)

        # Now substitute with the variables in mapping
        for string in to_replace:
            var = _get_var_regex.findall(string)[0]
            text = text.replace(string, mapping.get(var))

        return text
