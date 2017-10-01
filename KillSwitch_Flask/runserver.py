"""
This script runs the KillSwitch_Flask application using a development server.
"""

from os import environ
from KillSwitch_Flask import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)
