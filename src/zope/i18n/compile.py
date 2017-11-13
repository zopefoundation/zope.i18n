from contextlib import closing
import logging
import os
from os.path import join
from stat import ST_MTIME

HAS_PYTHON_GETTEXT = True
try:
    from pythongettext.msgfmt import Msgfmt
    from pythongettext.msgfmt import PoSyntaxError
except ImportError:
    HAS_PYTHON_GETTEXT = False

logger = logging.getLogger('zope.i18n')


def compile_mo_file(domain, lc_messages_path):
    """Creates or updates a mo file in the locales folder."""
    if not HAS_PYTHON_GETTEXT:
        logger.critical("Unable to compile messages: Python `gettext` library missing.")
        return

    base = join(lc_messages_path, domain)
    pofile = str(base + '.po')
    mofile = str(base + '.mo')

    po_mtime = 0
    try:
        po_mtime = os.stat(pofile)[ST_MTIME]
    except (IOError, OSError):
        return

    mo_mtime = 0
    if os.path.exists(mofile):
        # Update mo file?
        try:
            mo_mtime = os.stat(mofile)[ST_MTIME]
        except (IOError, OSError):
            return

    if po_mtime > mo_mtime:
        try:
            # Msgfmt.getAsFile returns io.BytesIO on Python 3, and cStringIO.StringIO
            # on Python 2; sadly StringIO isn't a proper context manager, so we have to
            # wrap it with `closing`. Also, Msgfmt doesn't properly close a file
            # it opens for reading if you pass the path, but it does if you pass
            # the file.
            with closing(Msgfmt(open(pofile, 'rb'), domain).getAsFile()) as mo:
                with open(mofile, 'wb') as fd:
                    fd.write(mo.read())
        except PoSyntaxError as err:
            logger.warning('Syntax error while compiling %s (%s).', pofile, err.msg)
        except (IOError, OSError) as err:
            logger.warning('Error while compiling %s (%s).', pofile, err)
