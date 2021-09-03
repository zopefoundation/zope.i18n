# This gives a linting error because unicode is not defined on Python 3:
# text_type = str if bytes is not str else unicode
try:
    # Python 2
    text_type = unicode
except NameError:
    # Python 3
    text_type = str
