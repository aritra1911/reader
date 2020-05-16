from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
)

# Remove unnecessary whitespace from Jinja rendered template
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from . import views
