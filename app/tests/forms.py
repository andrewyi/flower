# coding: utf-8

from datetime import datetime

from flask import (
    current_app,
    )

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import (
        Optional,
        InputRequired,
        ValidationError,
        Length,
        NumberRange,
    )


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
