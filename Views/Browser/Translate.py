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
"""Translation GUI

$Id: Translate.py,v 1.2 2002/06/13 14:04:58 srichter Exp $
"""
from Zope.Publisher.Browser.BrowserView import BrowserView
from Zope.App.PageTemplate import ViewPageTemplateFile
from Zope.I18n.ITranslationService import ITranslationService


class Translate(BrowserView):
    """ """
    
    __used_for__ = ITranslationService


    index = ViewPageTemplateFile('translate.pt')


    def getMessages(self):
        """Get messages based on the domain selection"""
        filter = self.request.get('filter', '%')
        domains = self.getEditDomains()
        messages = []
        for domain in domains:
            for msg_id in self.context.getMessageIdsOfDomain(domain, filter):
                messages.append((msg_id, domain, len(messages)))

        return messages


    def getTranslation(self, domain, msgid, target_lang):
        """ """
        return self.context.translate(domain, msgid,
                                      target_language=target_lang)
    

    def getAllLanguages(self):
        """Get all available languages from the Translation Service."""
        return self.context.getAllLanguages()


    def getAllDomains(self):
        return self.context.getAllDomains()
        

    def getEditLanguages(self):
        '''get the languages that are selected for editing'''
        languages = self.request.cookies.get('edit_languages', '')
        return filter(None, languages.split(','))


    def getEditDomains(self):
        '''get the languages that are selected for editing'''
        domains = self.request.cookies.get('edit_domains', '')
        return filter(None, domains.split(','))


    def editMessages(self):
        """ """
        # Handle new Messages
        for count in range(5):
            msg_id = self.request.get('new-msg_id-%i' %count, '')
            if msg_id:
                domain = self.request.get('new-domain-%i' %count, 'default')
                for language in self.getEditLanguages():
                    msg = self.request.get('new-%s-%i' %(language, count),
                                           msg_id)
                    self.context.addMessage(domain, msg_id, msg, language)

        # Handle edited Messages
        keys = filter(lambda k: k.startswith('edit-msg_id-'),
                      self.request.keys())
        keys = map(lambda k: k[12:], keys)
        for key in keys:
            msg_id = self.request['edit-msg_id-'+key]
            domain = self.request['edit-domain-'+key]
            for language in self.getEditLanguages():
                msg = self.request['edit-%s-%s' %(language, key)]
                if msg != self.context.translate(domain, msg_id,
                                                 target_language=language):
                    self.context.updateMessage(domain, msg_id, msg, language)
                
        return self.request.getResponse().redirect(self.request.URL[-1])


    def deleteMessages(self, message_ids):
        """ """
        for id in message_ids:
            domain = self.request.form['edit-domain-%s' %id]
            msgid = self.request.form['edit-msg_id-%s' %id]
            for language in self.context.getAvailableLanguages(domain):
                # Some we edit a language, but no translation exists...
                try:
                    self.context.deleteMessage(domain, msgid, language)
                except KeyError:
                    pass
        return self.request.getResponse().redirect(self.request.URL[-1])


    def addLanguage(self, language):
        """ """
        self.context.addLanguage(language)
        return self.request.getResponse().redirect(self.request.URL[-1])


    def addDomain(self, domain):
        """ """
        self.context.addDomain(domain)
        return self.request.getResponse().redirect(self.request.URL[-1])


    def changeEditLanguages(self, languages=[]):
        """ """
        self.request.getResponse().setCookie('edit_languages',
                                             ','.join(languages))
        return self.request.getResponse().redirect(self.request.URL[-1])


    def changeEditDomains(self, domains=[]):
        """ """
        self.request.getResponse().setCookie('edit_domains', ','.join(domains))
        return self.request.getResponse().redirect(self.request.URL[-1])


    def changeFilter(self):
        """ """
        filter = self.request.get('filter', '%')
        self.request.getResponse().setCookie('filter', filter)
        return self.request.getResponse().redirect(self.request.URL[-1])


    def deleteLanguages(self, languages):
        """ """
        for language in languages:
            self.context.deleteLanguage(language)
        return self.request.getResponse().redirect(self.request.URL[-1])


    def deleteDomains(self, domains):
        """ """
        for domain in domains:
            self.context.deleteDomain(domain)
        return self.request.getResponse().redirect(self.request.URL[-1])


