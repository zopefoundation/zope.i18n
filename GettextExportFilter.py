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
"""Translation Service Message Export Filter 

$Id: GettextExportFilter.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""
import time
from types import StringTypes

from Zope.I18n.IMessageExportFilter import IMessageExportFilter
from Zope.I18n.ITranslationService import IWriteTranslationService


class GettextExportFilter:

    __implements__ =  IMessageExportFilter
    __used_for__ = IWriteTranslationService


    def __init__(self, service):
        self.service = service

    ############################################################
    # Implementation methods for interface
    # Zope.I18n.IMessageExportFilter.IMessageExportFilter

    def exportMessages(self, domains, languages):
        'See Zope.I18n.IMessageExportFilter.IMessageExportFilter'

        if isinstance(domains, StringTypes):
            domain = domains
        elif len(domains) == 1:
            domain = domains[0]
        else:
            raise TypeError, \
                  'Only one domain at a time is supported for gettext export.'

        if isinstance(languages, StringTypes):
            language = languages
        elif len(languages) == 1:
            language = languages[0]
        else:
            raise TypeError, \
                'Only one language at a time is supported for gettext export.'

        dt = time.time()
        dt = time.localtime(dt)
        dt = time.strftime('%Y/%m/%d %H:%M', dt)
        output = _file_header %(dt, language.encode('UTF-8'),
                                domain.encode('UTF-8'))
        service = self.service

        for msgid in service.getMessageIdsOfDomain(domain):
            msgstr = service.translate(domain, msgid,
                                       target_language=language)
            msgstr = msgstr.encode('UTF-8')
            msgid = msgid.encode('UTF-8')
            output += _msg_template %(msgid, msgstr)

        return output        

    #
    ############################################################



_file_header = '''
msgid ""
msgstr ""
"Project-Id-Version: Zope 3\\n"
"PO-Revision-Date: %s\\n"
"Last-Translator: Zope 3 Gettext Export Filter\\n"
"Zope-Language: %s\\n"
"Zope-Domain: %s\\n" 
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
'''

_msg_template = '''
msgid "%s"
msgstr "%s"
'''
