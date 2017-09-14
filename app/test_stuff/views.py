# coding: utf-8
'''
app.test_stuff.views
------------------

随便怎么整的东西

'''

from flask import (
    current_app,
    request,
)

from . import test_stuff
from .. import csrf


@test_stuff.route('/test_a', methods=['GET', 'POST'])
@csrf.exempt
def test_a():
    if not request.json:
        request.json = {}
    current_app.logger.error('requst.json: %s.', request.json)
    return 'ok'
