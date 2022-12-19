import os
import sys

sys.path.insert(0, '/usr/home/ray/pgm/reader/flask')
from constants import PREFIX

activate_this = os.path.join(PREFIX, 'virtualenv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from src import app as application
