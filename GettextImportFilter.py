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
"""Translation Service Message Import Filter 

$Id: GettextImportFilter.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""
import time, re
from types import StringTypes

from Zope.I18n.IMessageImportFilter import IMessageImportFilter
from Zope.I18n.ITranslationService import IWriteTranslationService


class GettextImportFilter:

    __implements__ =  IMessageImportFilter
    __used_for__ = IWriteTranslationService


    def __init__(self, service):
        self.service = service

    ############################################################
    # Implementation methods for interface
    # Zope.I18n.IMessageImportFilter.IMessageImportFilter

    def importMessages(self, domains, languages, file):
        'See Zope.I18n.IMessageImportFilter.IMessageImportFilter'

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

        result = parseGetText(file.readlines())[3]
        headers = parserHeaders(''.join(result[('',)][1]))
        del result[('',)]
        charset = extractCharset(headers['content-type'])
        service = self.service
        for msg in result.items():
            msgid = unicode(''.join(msg[0]), charset)
            msgid = msgid.replace('\\n', '\n')
            msgstr = unicode(''.join(msg[1][1]), charset)
            msgstr = msgstr.replace('\\n', '\n')
            service.addMessage(domain, msgid, msgstr, language)

    #
    ############################################################


def extractCharset(header):
    charset = header.split('charset=')[-1]
    return charset.lower()


def parserHeaders(headers_text):
    headers = {}
    for line in headers_text.split('\\n'):
        name = line.split(':')[0]
        value = ''.join(line.split(':')[1:])
        headers[name.lower()] = value

    return headers


def parseGetText(content):
    # The regular expressions
    com = re.compile('^#.*')
    msgid = re.compile(r'^ *msgid *"(.*?[^\\]*)"')
    msgstr = re.compile(r'^ *msgstr *"(.*?[^\\]*)"') 
    re_str = re.compile(r'^ *"(.*?[^\\])"') 
    blank = re.compile(r'^\s*$')

    trans = {}
    pointer = 0
    state = 0
    COM, MSGID, MSGSTR = [], [], []
    while pointer < len(content):
        line = content[pointer]
        #print 'STATE:', state
        #print 'LINE:', line, content[pointer].strip()
        if state == 0:
            COM, MSGID, MSGSTR = [], [], []
            if com.match(line):
                COM.append(strip(line))
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                MSGID.append(msgid.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 0, line %d\n' % (pointer + 1)
        elif state == 1:
            if com.match(line):
                COM.append(strip(line))
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                MSGID.append(msgid.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 1, line %d\n' % (pointer + 1)

        elif state == 2:
            if com.match(line):
                COM.append(strip(line))
                state = 2
                pointer = pointer + 1
            elif re_str.match(line):
                MSGID.append(re_str.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif msgstr.match(line):
                MSGSTR.append(msgstr.match(line).group(1))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 2, line %d\n' % (pointer + 1)

        elif state == 3:
            if com.match(line) or msgid.match(line):
                # print "\nEn", language, "detected", MSGID
                trans[tuple(MSGID)] = (COM, MSGSTR)
                state = 0
            elif re_str.match(line):
                MSGSTR.append(re_str.match(line).group(1))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 3, line %d\n' % (pointer + 1)

    # the last also goes in
    if tuple(MSGID):
        trans[tuple(MSGID)] = (COM, MSGSTR)

    return COM, MSGID, MSGSTR, trans
