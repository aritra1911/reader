from . import app
from .journal import JournalEntry
from flask import render_template
from os import environ, sep, listdir, path

PATH=environ['JOURNAL_DIR']

@app.route("/")
def index():
    return render_template("index.html", files=[
        f
        for f in listdir(PATH)
        if path.isfile(path.join(PATH, f)) and f.endswith('.jrl')
    ])

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry(PATH + sep + filename)
    return render_template("journal.html",
        title=entry.get_title(),
        body=entry.get_paragraphs(),
    )
