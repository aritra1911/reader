from . import app
from .journal import JournalEntry
from .helpers import cycle
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
    entry = JournalEntry()
    entry.set_filename(PATH + sep + filename)

    # Decrypt file
    entry.read_file(decrypt=lambda msg: ''.join([
        chr((ord(c) - (65 if not c.islower() else 97) - (ord(s) - 97)) % 26
        + (65 if not c.islower() else 97)) if c.isalpha() else c
        for c, s in zip(msg, cycle(msg, 'lollipop'))
    ]))

    entry.parse()

    return render_template("journal.html",
        title=entry.get_title(),
        body=entry.get_paragraphs(),
    )
