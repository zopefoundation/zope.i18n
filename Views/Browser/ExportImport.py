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
"""Message Export/Import View

$Id: ExportImport.py,v 1.1 2002/06/16 18:25:13 srichter Exp $
"""

from Zope.ComponentArchitecture import getAdapter

from Zope.App.PageTemplate import ViewPageTemplateFile
from Zope.I18n.IMessageExportFilter import IMessageExportFilter
from Zope.I18n.IMessageImportFilter import IMessageImportFilter

from BaseTranslationServiceView import BaseTranslationServiceView

class ExportImport(BaseTranslationServiceView):
    """ """
    
    exportImportForm = ViewPageTemplateFile('exportImport.pt')


    def exportMessages(self, domains, languages):
        self.request.getResponse().setHeader('content-type',
                                             'application/x-gettext')
        filter = getAdapter(self.context, IMessageExportFilter)
        return filter.exportMessages(domains, languages)
        
    
    def importMessages(self, domains, languages, file):
        filter = getAdapter(self.context, IMessageImportFilter)
        filter.importMessages(domains, languages, file)
        return self.request.getResponse().redirect(self.request.URL[-1])

    
