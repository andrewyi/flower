# coding: utf-8
'''
app.tests.views
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
    render_template_string,
    session,
    Response,
)

from . import tests
from . import forms

from .. import csrf, limiter
from ..accessory.auth_util import check_auth

@tests.route('/xml')
def test_xml():
    content = '<?xml version="1.0" ?><xml><value>heiheihei</value></xml>'
    return Response(content, mimetype='text/xml')

@tests.route('/checkbox', methods=['GET', 'POST'])
@csrf.exempt
def test_checkbox():
    if request.method == 'GET':
        return render_template_string('''
        <head>
        </head>
        <body>
            <form method="POST" action="{{ url_for('tests.test_checkbox') }}">
            <input type="checkbox" name="checkbox_test" value="content_goes_here" checked="checked">ang</input>
            <input type="submit" name="tijiao">
            </form>
        </body>
        ''')
    else:
        current_app.logger.error('checkbox_test -----%s.', request.form.get('checkbox_test'))
    return 'OK'


@tests.route('/host')
def test_host():
    current_app.logger.error('url-----%s.', request.url)
    current_app.logger.error('url_root-----%s.', request.url_root)
    current_app.logger.error('host-----%s.', request.host)
    current_app.logger.error('path-----%s.', request.path)
    current_app.logger.error('remote_addr-----%s.', request.remote_addr)
    return 'OK'


@tests.route('/delete', methods=['DELETE'])
def test_delete():
    form = forms.TestDeleteForm(request.form)
    if not form.validate():
        current_app.logger.error('form validate error: %s.', form.errors)
        return jsonify(code=500, message='form error')

    return jsonify(code=0, message=form.text.data)


@tests.route('/session')
def test_session():
    msg = request.args.get('msg')
    if msg:
        session['msg'] = request.args.get('msg')
    return session.get('msg', 'not avaiable')

@tests.route('/ep')
@check_auth
def test_endopint():
    return request.endpoint


@tests.route('/test_abort')
@csrf.exempt
def test_abort():
    code = request.args.get('code')
    try:
        code = int(code)
    except:
        code = 400

    import time
    # time.sleep(3)

    if code >= 400:
        current_app.logger.info('gonna abort(%s).', code)
        abort(code)
    else:
        return make_response('return with code', code)

    return 'ok'


@tests.errorhandler(400)
def invalid_params_handler(e):
    return make_response(jsonify(code=400, message='访问参数有误'), 200)


@tests.route('/fieldlist', methods=['GET'])
@csrf.exempt
def fieldlist():
    form = forms.InsuranceQuoteAddForm()

    # form.insurance_company_id.data = 99999

    nuf = forms.NotifyUserForm()
    # nuf.user_id = 1000
    form.notify_user_fields.append_entry(nuf)

    iif = forms.InsuranceItemForm()
    form.insurance_item_fields.append_entry(iif)

    cbf = forms.CouponBatchForm()
    form.coupon_fields.append_entry(cbf)

    return render_template_string(
    '''
    {{ form.insurance_company_id.name }} ===  {{ form.insurance_company_id.data }}
    <br/>
    {% for i in form.notify_user_fields %}
    {{ i.user_id.name }} ==== {{ i.user_id.data }}
    <br/>
    {% endfor %}
    {% for i in form.coupon_fields %}
    {{ i.coupon_batch_id.name }} ==== {{ i.coupon_batch_id.data }} |||| {{ i.coupon_count.name }} ==== {{ i.coupon_count.data }}
    <br/>
    {% endfor %}
    -------------------------
    <br/>
    {% for i in form.insurance_item_fields %}
    {{ i.insurance_kind_id.name }} ==== {{ i.insurance_kind_id.data }}
    <br/>
    {{ i.count.name }} ==== {{ i.count.data }}
    <br/>
    {{ i.unit.name }} ==== {{ i.unit.data }}
    <br/>
    {{ i.glass_type.name }} ==== {{ i.glass_type.data }}
    <br/>
    {{ i.coverage.name }} ==== {{ i.coverage.data }}
    <br/>
    {{ i.coverage_unit.name }} ==== {{ i.coverage_unit.data }}
    <br/>
    {{ i.price.name }} ==== {{ i.price.data }}
    <br/>
    {{ i.is_selected.name }} ==== {{ i.is_selected.data }}
    <br/>
    {% endfor %}
    ''',
    form=form
    )


@csrf.error_handler
def csrf_error(reason):
    current_app.logger.error('-----------------: %s.', reason)
    abort(400)
    return render_template_string('csrf_error: {{ reason }}.', reason=reason), 400


@tests.route('/form', methods=['POST'])
# @csrf.exempt
def form_parameters():
    form = forms.ParamForm()
    # form.csrf_enabled = False

    if not form.validate_on_submit():
        current_app.logger.error(
                'form.validate_on_submit failed, error: %s.', form.errors)
    var1 = form.var1.data
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))

    # form.var1.data = 666666
    # current_app.logger.error('-=-=-=-=-=-=-=-=-=-= form.vat1: %s.', form.var1.data)

    return 'form'


@tests.route('/post', methods=['POST'])
@csrf.exempt
def post_parameters():
    var1 = request.form.get('var1', type=int, default=8888)
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))
    return 'post'


@tests.route('/get')
def get_parameters():
    var1 = request.args.get('var1', type=int, default=77777)
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))
    return 'get'


@tests.route('/echo')
def do_echo():
    q = request.args.get('q')
    current_app.logger.info('get q: %s.', q)
    # return q
    if q == 'hehe':
        return jsonify(echo=q)


@tests.route('/exception')
def raise_exp():
    e = request.args.get('e')
    current_app.logger.info('get e: %s.', e)
    raise Exception(e)
    return ''

class T(object):
    def __init__(self, v):
        self.v = v

@tests.route('/render')
def render():
    # args = {'test_key':'test_value'}
    t = T('test args ..........')
    return render_template('tests/index.html', args=t)

@jinja2.contextfilter
@tests.app_template_filter()
def cvalue(context, t):
    return ('cvalue converted input: %s' % (t.v,))

@tests.app_context_processor
def fvalue_wrapper():
    def fvalue(t):
        return ('fvalue converted input: %s' % (t.v,))
    return dict(fvalue=fvalue)


@tests.app_template_filter()
def test_cross(v):
    return 'test_cross(%s)' % (str(v),)

@tests.app_context_processor
def asdfasdf():
    return dict(v='asdfasdfasdfasdfasdfdsvvvvvv')


@tests.app_errorhandler(501)
def error_handler(error):
    current_app.logger.error('----error is : %s, %s.', error, type(error))
    return 'error_handler for 501'

from ..accessory.facilities import TestException
@tests.app_errorhandler(TestException)
def exception_handler(error):
    current_app.logger.error('----error is : %s, %s.', error, type(error))
    return 'error_handler for exception TestException'


@tests.route('/login')
def login():
    current_app.logger.info('login')
    return jsonify(code=0, message='ok', ext='login success')


@tests.route('/work', methods=['POST'])
@csrf.exempt
def work():
    number = request.form.get('number', type=int, default=0)
    current_app.logger.info('work, number: %s.', number)
    return jsonify(code=0, message='ok', ext='work success')


@tests.route('/limit', methods=['GET'])
@limiter.limit('2/60seconds')
def limit_test():
    return 'OK'

@tests.errorhandler(429)
def ratelimit_error_handler(e):
    return make_response(jsonify(code=429, message='您的访问太频繁了'), 200)
