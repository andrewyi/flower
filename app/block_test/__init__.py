from flask import Blueprint

block_test = Blueprint('block_test', __name__)

from . import views
