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

$Id: test_messageid.py,v 1.4 2003/08/18 19:20:23 srichter Exp $
"""

import unittest
from zope.i18n.messageid import MessageIDFactory, MessageID


class TestMessageID(unittest.TestCase):
    def testMessageIDFactory(self):
        eq = self.assertEqual
        fact = MessageIDFactory('test')
        id = fact(u'this is a test')
        self.failUnless(isinstance(id, MessageID))
        self.failUnless(isinstance(id, unicode))
        eq(id.domain, 'test')
        eq(id.default, u'this is a test')
        id.default = u'blah'
        eq(id.default, u'blah')
        id = fact(u'test-id', 'default test')
        eq(id, u'test-id')
        eq(id.default, u'default test')
        eq(id.domain, 'test')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMessageID))
    return suite


if __name__ == '__main__':
    unittest.main()
