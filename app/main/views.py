from . import main

from flask import render_template

@main.route('/')
def root():
    return render_template('main/index.html')
