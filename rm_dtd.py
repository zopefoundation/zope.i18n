##############################################################################
#
# Copyright (c) 2002, 2003 Zope Corporation and Contributors.
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
"""Removes the DOCTYPE line from the Locale XML Files.

$Id: rm_dtd.py,v 1.2 2003/05/01 19:35:42 faassen Exp $
"""
import os
from zope import i18n

locale_dir = os.path.join(os.path.dirname(i18n.__file__), 'locales')

for file in filter(lambda f: f.endswith('.xml'),
                   os.listdir(locale_dir)):
    path = os.path.join(locale_dir, file)
    print path
    data = open(path, 'r').read()
    data = data.replace(
        '<!DOCTYPE localeData SYSTEM "./LocaleElements.dtd" >\n', '')
    open(path, 'w').write(data)
