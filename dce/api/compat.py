# coding=utf-8
import sys

'''
This module ensure compatibility between Python 2 and 
Python 3.
'''

_ver = sys.version_info
is_PY2 = (_ver[0] == 2)
is_PY3 = (_ver[0] == 3)


if is_PY2:
    from urlparse import urlparse, urljoin
    from urllib import quote_plus

    range_ = xrange
    string_types = basestring
    numeric_types = (int, long, float)

elif is_PY3:
    from urllib.parse import urlparse, quote_plus, urljoin

    range_ = range
    string_types = str
    numeric_types = (int, float)

