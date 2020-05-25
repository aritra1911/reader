from . import app
from .journal import JournalEntry
from .helpers import get_decrypt_func
from flask import render_template, request, session, url_for, redirect
from os import environ, sep, listdir, path
import re

PATH = environ['JOURNAL_DIR']

def redirect_dest(fallback):
    kwargs = request.args.copy()
    try:
        dest = kwargs.pop('next')
    except KeyError:
        dest = None

    try:
        dest_url = url_for(dest, **kwargs)
    except TypeError:
        return redirect(fallback)
    return redirect(dest_url)

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

    try:
        key = session['key']
    except KeyError:
        key = None

    for file in files:
        entry.set_filename(PATH + sep + file)

        # You might ask why on earth I'm not optimising read_file() to just get
        # the title in this case. Well, I ran a few tests and recorded the times
        # they took to load the file_content. Apparently there's not much
        # advantage in doing that. Also somehow reading the file line by line
        # wasn't actually quicker than dumping it all at once into a variable.
        # I'm also using a single object here in order to cut down on some memory
        # usage.
        entry.read_file(decrypt=get_decrypt_func(key))
        entry.parse()
        journals[file] = entry.get_title()

    return render_template('index.html',
        journals_menu=journals,
        key_exists=(key is not None)
    )

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry()
    entry.set_filename(PATH + sep + filename)
    try:
        key = session['key']
    except KeyError:
        key = None
    entry.read_file(decrypt=get_decrypt_func(key))
    entry.parse()

    return render_template("journal.html",
        filename=entry.get_filename(),
        title=entry.get_title(),
        body=entry.get_paragraphs(),
        date=entry.get_date('%B %d, %Y'),
        key_exists=(key is not None)
    )

@app.route('/enterkey', methods=('GET', 'POST'))
def enter_key():
    if request.method == 'POST':
        session.clear()

        # '\W' pulls out all non-alphanumeric characters
        # '\d' pulls out all numeric characters
        key_regex = re.compile('[\W\d_]+')
        key = key_regex.sub('', request.form['key'].lower())
        if key:
            session['key'] = key

        return redirect_dest(fallback=url_for('index'))

    return render_template('enterkey.html')

@app.route('/removekey')
def remove_key():
    session.clear()
    return redirect_dest(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
