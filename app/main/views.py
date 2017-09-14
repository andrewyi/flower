from flask import current_app

from . import main


@main.route('/')
def root():
    current_app.logger.info('in main, root')
    return 'ok'

@main.route('/health')
def health():
    current_app.logger.info('in main, health')
    return 'ok'
