##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Message ID tests.

$Id: test_messageid.py,v 1.5 2004/02/20 09:24:38 philikon Exp $
"""

import unittest
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('zope.i18n.messageid'),
        ))

if __name__ == '__main__':
    unittest.main()
