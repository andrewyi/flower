# coding: utf-8
'''
app.form.views
------------------

'''

from flask import (
    current_app,
    request,
    jsonify,
    # render_template,
    render_template_string,
)

from . import form
from . import forms
from .. import csrf


@form.route('/checkbox', methods=['GET', 'POST'])
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


@form.route('/delete', methods=['DELETE'])
def test_delete():
    form = forms.TestDeleteForm(request.form)
    if not form.validate():
        current_app.logger.error('form validate error: %s.', form.errors)
        return jsonify(code=500, message='form error')

    return jsonify(code=0, message=form.text.data)


@form.route('/fieldlist', methods=['GET'])
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


@form.route('/form', methods=['POST'])
@csrf.exempt
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


@form.route('/post', methods=['POST'])
@csrf.exempt
def post_parameters():
    var1 = request.form.get('var1', type=int, default=8888)
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))
    return 'post'


@form.route('/nullable_test', methods=['POST'])
@csrf.exempt
def nullable_test():
    f = forms.NullableTestForm(csrf_enabled=False)
    if not f.validate_on_submit():
        current_app.logger.error(
                'form.validate_on_submit failed, error: %s.', f.errors)
        return 'validate_on_submit error'
    current_app.logger.error('value: %s.', f.d.data)

    return 'OK'
