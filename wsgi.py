import os
from app import create_app


application = create_app(os.getenv('FLASK_ENV'))
