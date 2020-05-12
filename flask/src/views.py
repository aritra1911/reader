from . import app
from .journal import JournalEntry
from flask import render_template
from os import environ, sep

@app.route("/")
def index():
    return "HelloWorld!"

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry(environ['JOURNAL_PATH'] + sep + filename)
    return render_template("journal.html",
        title=entry.get_title(),
        body=entry.get_paragraphs(),
    )
