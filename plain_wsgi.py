# -*- python sources -*-

import logging
logger = logging.getLogger()

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    logger.error('-----------------------------------------')
    for k, v in env.items():
        logger.error('%s\t\t\t:\t\t\t%s', k, v)
    return (b'ok',)
