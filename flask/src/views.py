from . import app
from .journal import JournalEntry
from .helpers import cycle
from flask import render_template
from os import environ, sep, listdir, path

# TODO, Move these to `constants.py`
PATH = environ['JOURNAL_DIR']
DECRYPT_FUNC = lambda msg: ''.join([
    chr((ord(c) - (65 if not c.islower() else 97) - (ord(s) - 97)) % 26
    + (65 if not c.islower() else 97)) if c.isalpha() else c
    for c, s in zip(msg, cycle(msg, 'lollipop'))
])

@app.route("/")
def index():
    files = [
        f
        for f in listdir(PATH)
        if path.isfile(path.join(PATH, f)) and f.endswith('.jrl')
    ]
    files.sort()

    entry = JournalEntry()
    journals = dict()  # journals['filename': 'title']
    for file in files:
        entry.set_filename(PATH + sep + file)

        # You might ask why on earth I'm not optimising read_file() to just get
        # the title in this case. Well, I ran a few tests and recorded the times
        # they took to load the file_content. Apparently there's not much
        # advantage in doing that. Also somehow reading the file line by line
        # wasn't actually quicker than dumping it all at once into a variable.
        # I'm also using a single object here in order to cut down on some memory
        # usage.
        entry.read_file(decrypt=DECRYPT_FUNC)
        entry.parse()
        journals.update({file: entry.get_title()})

    return render_template('index.html', journals_menu=journals)

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry()
    entry.set_filename(PATH + sep + filename)

    entry.read_file(decrypt=DECRYPT_FUNC)
    entry.parse()

    return render_template("journal.html",
        title=entry.get_title(),
        body=entry.get_paragraphs(),
    )
