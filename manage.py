#!/usr/bin/env python

import os
from flask_script import Manager

from app import create_app
from app.command import ServiceCommand

app = create_app(os.getenv('FLASK_ENV'))
manager = Manager(app)

manager.add_command('service', ServiceCommand)

if __name__ == '__main__':
    manager.run()
