
activate_this = '/usr/home/ray/pgm/reader/flask/virtualenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/usr/home/ray/pgm/reader/flask')

from src import app as application

