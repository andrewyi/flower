from . import main

from flask import render_template, current_app

@main.route('/')
def root():
    current_app.logger.info('in main')
    return render_template('main/index.html')
