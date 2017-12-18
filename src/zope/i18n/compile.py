from contextlib import closing
import os.path
from os.path import join
import logging

from pythongettext.msgfmt import Msgfmt
from pythongettext.msgfmt import PoSyntaxError

logger = logging.getLogger('zope.i18n')


HAS_PYTHON_GETTEXT = True

def _safe_mtime(path):
    try:
        return os.path.getmtime(path)
    except (IOError, OSError):
        return None

def compile_mo_file(domain, lc_messages_path):
    """Creates or updates a mo file in the locales folder."""

    base = join(lc_messages_path, domain)
    pofile = str(base + '.po')
    mofile = str(base + '.mo')

    po_mtime = _safe_mtime(pofile)
    mo_mtime = _safe_mtime(mofile) if os.path.exists(mofile) else 0

    if po_mtime is None or mo_mtime is None:
        logger.debug("Unable to access either %s (%s) or %s (%s)",
                     pofile, po_mtime, mofile, mo_mtime)
        return

    if po_mtime > mo_mtime:
        try:
            # Msgfmt.getAsFile returns io.BytesIO on Python 3, and cStringIO.StringIO
            # on Python 2; sadly StringIO isn't a proper context manager, so we have to
            # wrap it with `closing`. Also, Msgfmt doesn't properly close a file
            # it opens for reading if you pass the path, but it does if you pass
            # the file.
            with open(pofile, 'rb') as pofd:
                with closing(Msgfmt(pofd, domain).getAsFile()) as mo:
                    with open(mofile, 'wb') as fd:
                        fd.write(mo.read())
            # For testing we return distinct values for each scenario
            return True
        except PoSyntaxError as err:
            logger.warning('Syntax error while compiling %s (%s).', pofile, err.msg)
            return 0
        except (IOError, OSError) as err:
            logger.warning('Error while compiling %s (%s).', pofile, err)
            return False
