##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import unittest

from zope.i18n import compile


@unittest.skipUnless(compile.HAS_PYTHON_GETTEXT,
                     "Need python-gettext")
class TestCompile(unittest.TestCase):

    def test_non_existant_path(self):

        self.assertIsNone(compile.compile_mo_file('no_such_domain', ''))

    def test_po_exists_but_invalid(self):
        import tempfile
        import shutil
        import os.path

        td = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, td)

        with open(os.path.join(td, "foo.po"), 'w') as f:
            f.write("this should not compile")

        self.assertEqual(
            0,
            compile.compile_mo_file('foo', td))

    def test_po_exists_cannot_write_mo(self):
        import tempfile
        import shutil
        import os
        import os.path

        td = tempfile.mkdtemp(suffix=".zopei18n_test_compile")
        self.addCleanup(shutil.rmtree, td)

        mofile = os.path.join(td, 'foo.mo')
        with open(mofile, 'w') as f:
            f.write("Touching")

        # Put it in the past, make it not writable
        os.utime(mofile, (1000, 1000))
        os.chmod(mofile, 0)

        with open(os.path.join(td, "foo.po"), 'w') as f:
            f.write("# A comment")

        self.assertIs(
            False,
            compile.compile_mo_file('foo', td))

    def test_cannot_compile(self):
        self.assertIsNone(compile._cannot_compile_mo_file(None, None))
