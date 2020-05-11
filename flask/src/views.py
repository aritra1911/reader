from . import app
from .journal import JournalEntry
from flask import render_template

PARENT_PATH = "/home/ray/codes/python/flask/reader/flask/src"
SEP = '/'

@app.route("/")
def index():
    return "HelloWorld!"

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry(PARENT_PATH + SEP + filename)
    return render_template("journal.html",
        title=entry.get_title(),
        body=entry.get_paragraphs(),
    )
