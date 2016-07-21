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
    )


class ParamForm(Form):
    var1 = StringField('var1', default="var1---", validators=[InputRequired()])
    var2 = IntegerField('var2', validators=[Optional()])
    var3 = DateField('var3', default=datetime(2011,1,1), validators=[InputRequired()])

    def validate_var2(form, field):
        current_app.logger.error('##################################')
        raise ValidationError('heeh')
