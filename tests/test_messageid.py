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

$Id: test_messageid.py,v 1.1 2003/03/25 00:23:05 slinkp Exp $
"""

import unittest
from zope.i18n.messageid import MessageIDFactory, MessageID

class TestMessageID(unittest.TestCase):
    def test(self):
        fact = MessageIDFactory('test')
        id = fact(u'this is a test')
        self.assert_(isinstance(id, MessageID))
        self.assertEqual(id.domain, 'test')
        self.assertEqual(id.default, None)
        id.setDefault(u'blah')
        self.assertEqual(id.default, u'blah') 


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMessageID))
    return suite


if __name__ == '__main__':
    unittest.main()
