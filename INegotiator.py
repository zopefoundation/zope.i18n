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

$Id: INegotiator.py,v 1.3 2002/06/12 15:55:33 bwarsaw Exp $
"""

from Interface import Interface

class INegotiator(Interface):

    """A language negotiation service.
    """
  
    def getLanguage(langs, env):
        """Return the matching language to use.

        The decision of which language to use is based on the list of
        available languages, and the given user environment.  An
        IUserPreferredLanguages adapter for the environment is obtained and
        the list of acceptable languages is retrieved from the environment.

        If no match is found between the list of available languages and the
        list of acceptable languages, None is returned.

        Arguments:

        langs -- sequence of languages (not necessarily ordered)

        env  -- environment passed to the service to determine a sequence
                of user prefered languages
        """

        # XXX I'd like for there to be a symmetric interface method, one in
        # which an adaptor is gotten for both the first arg and the second
        # arg.  I.e. getLanguage(obj, env)
        # But this isn't a good match for the iTranslationService.translate()
        # method. :(
