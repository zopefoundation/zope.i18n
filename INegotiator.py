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

$Id: INegotiator.py,v 1.2 2002/06/10 23:29:28 jim Exp $
"""

from Interface import Interface

class INegotiator(Interface):

    """ The INegotiater defines an interface for a service for language 
       negotiation
    """
  
    def getLanguage(object_langs,  env):
        """getLanguage implements a decision making algorithm to decide
           what language should be used based on the available languages
           for an object and a list of user prefered languages.

        Arguments:

        object_langs -- sequence of languages (not necessarily ordered)

        env  -- environment passed to the service to determine a sequence
                of user prefered languages

        """

