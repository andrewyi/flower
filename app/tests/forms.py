# coding: utf-8

from datetime import datetime

from flask import (
    current_app,
    )

from flask_wtf import Form
from wtforms import FormField, FieldList, StringField, IntegerField, DateField, BooleanField
from wtforms.validators import (
        Optional,
        InputRequired,
        ValidationError,
        Length,
        NumberRange,
    )

class TestDeleteForm(Form):
    text = StringField('text')


class ParamForm(Form):
    '''
    var1 = StringField('var1', default="var1---", validators=[InputRequired(message='input required'), Length(min=2, message='length min is 2')])
    var1 = StringField('var1', default="var1---", validators=[Optional(), Length(min=2, message='length min is 2')])

    def validate_var1(form, field):
        current_app.logger.error('in validator ###')
        raise ValidationError('in validator ###')

    '''

    var1 = IntegerField('var1', default=7777, validators=[InputRequired(message='input required'), NumberRange(min=2, message='range min is 2')])
    # var1 = IntegerField('var1', default=7777, validators=[Optional(), NumberRange(min=2, message='range min is 2')])

    def validate_var1(form, field):
        current_app.logger.error('in validator ###')
        raise ValidationError('in validator ###')

    var2 = BooleanField('var2')

    def validate_var2(form, field):
        current_app.logger.error('in validator var2 ------ %s.', field.data)

class NotifyUserForm(Form):

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(NotifyUserForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

    user_id = IntegerField('用户id')


class InsuranceItemForm(Form):

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(InsuranceItemForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

    insurance_kind_id = IntegerField('保险项id')
    count = IntegerField('数值选项')
    unit = StringField('单位选项')
    glass_type = StringField('玻璃选项')
    coverage = StringField('保额选项')
    coverage_unit = StringField('保额单位选项')
    price = IntegerField('保费')
    is_selected = BooleanField('是否选择')


class CouponBatchForm(Form):

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(CouponBatchForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

    coupon_batch_id = IntegerField('优惠券批次id')
    coupon_count = IntegerField('发放数量')


class InsuranceQuoteAddForm(Form):
    quote_id = IntegerField('报价id')
    user_id = IntegerField('用户id')

    notify_user_fields = FieldList(FormField(NotifyUserForm), min_entries=0)

    insurance_company_id = IntegerField('保险公司id')
    insurance_effected_on = DateField('车险开始时间')
    insurance_expires_on = DateField('车险结束时间')

    insurance_item_fields = FieldList(FormField(InsuranceItemForm), min_entries=0)

    commercial_total_price = IntegerField('商业险保费合计')
    commercial_discount_rate = IntegerField('商业险保费折扣')
    # commercial_discount_amount = IntegerField('商业险折扣金额')

    commercial_ins_price = IntegerField('商业险折后保费')
    compulsory_ins_price = IntegerField('交强险保费')
    tax_ins_price = IntegerField('车船税税款')

    prepaid_amount = IntegerField('预存金')
    total_price = IntegerField('应付金额')

    coupon_fields = FieldList(FormField(CouponBatchForm), min_entries=0)
