from . import app
from src.read_file import get_file_content

@app.route("/")
def index():
    return "HelloWorld!"

@app.route("/file")
def display_file():
    return get_file_content()

