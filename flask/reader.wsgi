
activate_this = '/opt/ray/var/apache/httpd/www/reader/virtualenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/opt/ray/var/apache/httpd/www/reader')

from src import app as application

