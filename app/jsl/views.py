# coding: utf-8
'''
app.jsl.views
------------------

'''

import jinja2
from flask import (
    current_app,
    request,
    make_response,
    abort,
    jsonify,
    render_template,
)

from . import jsl

from .. import csrf
from ..accessory.auth_util import check_auth


@jsl.route('/index')
@check_auth
def test_endopint():
    return render_template('jsl/index.html')
