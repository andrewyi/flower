from flask import Blueprint

html_loading_blocking_test = Blueprint('html_loading_blocking_test', __name__)

from . import views
