# -*- coding: utf-8 -*-
"""
app.compat
----------

Python2和Python3兼容性处理
"""

import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)

is_py3 = (_ver[0] == 3)

if is_py2:
    from urllib import (
        quote,
        unquote,
        quote_plus,
        unquote_plus,
        urlencode
    )
    from urlparse import urlparse
elif is_py3:
    from urllib.parse import (
        quote,
        unquote,
        quote_plus,
        unquote_plus,
        urlparse,
        urlencode
    )
