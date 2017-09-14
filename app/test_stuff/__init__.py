from flask import Blueprint

test_stuff = Blueprint('test_stuff', __name__)

from . import views
