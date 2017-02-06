from . import main

from flask import render_template, current_app, jsonify

@main.route('/')
def root():
    current_app.logger.info('in main')
    return 'ok'
