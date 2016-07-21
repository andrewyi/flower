# coding: utf-8
'''
app.tests.views
------------------

'''

from flask import (
    current_app,
    request,
    make_response,
    abort,
    jsonify,
)

from . import tests
from . import forms

from .. import csrf


@tests.route('/test_abort')
@csrf.exempt
def test_abort():
    code = request.args.get('code')
    try:
        code = int(code)
    except:
        code = 400
    current_app.logger.error('gonna abort(%s).', code)
    abort(code)

    return 'ok'


@tests.errorhandler(400)
def invalid_params_handler(e):
    return make_response(jsonify(code=400, message='访问参数有误'), 200)


@tests.route('/form', methods=['POST'])
@csrf.exempt
def form_parameters():
    form = forms.ParamForm()
    form.csrf_enabled = False
    var1 = form.var1.data
    current_app.logger.debug('----> var1: %s.', var1)
    current_app.logger.debug('----> typeof var1: %s.', type(var1))

    current_app.logger.debug('');

    var2 = form.var2.data
    current_app.logger.debug('----> var2: %s.', var2)
    current_app.logger.debug('----> typeof var2: %s.', type(var2))

    current_app.logger.debug('');

    form = forms.ParamForm()
    var3 = form.var3.data
    current_app.logger.debug('----> var3: %s.', var3)
    current_app.logger.debug('----> typeof var3: %s.', type(var3))

    current_app.logger.debug('');
    form.validate_on_submit()
    current_app.logger.debug('from validte error: %s.', form.errors);
    current_app.logger.debug('');

    return 'form'


@tests.route('/post', methods=['POST'])
@csrf.exempt
def post_parameters():
    var1 = request.form.get('var1')
    current_app.logger.debug('----> var1: %s.', var1)
    current_app.logger.debug('----> typeof var1: %s.', type(var1))
    return 'post'


@tests.route('/get')
def get_parameters():
    var1 = request.args.get('var1')
    current_app.logger.debug('----> var1: %s.', var1)
    current_app.logger.debug('----> typeof var1: %s.', type(var1))
    return 'get'
