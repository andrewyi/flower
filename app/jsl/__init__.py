from flask import Blueprint

jsl = Blueprint('jsl', __name__)

from . import views
