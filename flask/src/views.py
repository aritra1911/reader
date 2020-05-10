from . import app
from .read_file import get_file_content
from .journal import JournalEntry

PARENT_PATH = "/home/ray/codes/python/flask/reader/flask/src"
SEP = '/'

@app.route("/")
def index():
    return "HelloWorld!"

@app.route("/file")
def display_file():
    return get_file_content()

@app.route("/<filename>")
def render_file(filename):
    entry = JournalEntry(PARENT_PATH + SEP + filename)
    res = "<h2>" + entry.get_title() + "</h2>"
    for paragraph in entry.get_paragraphs():
        res += "<p>"
        for line in paragraph:
            res += line + "<br />"
        res += "</p>"

    return res
