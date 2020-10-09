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

    # Sort `journals` dictionary in decending
    journals = {
        key: value
        for key, value in sorted(
            journals.items(),
            key=lambda item: item[0],
            reverse=True
        )
    }

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
    entry.to_html()

    prev, next = get_neighbours(filename)

    return render_template("journal.html",
        filename=entry.get_filename(),
        title=entry.get_title(),
        body=entry.get_html_paragraphs(),
        date=entry.get_date('%B %d, %Y -- %A'),
        key_exists=(key is not None),
        prev=prev,
        next=next,
    )

def get_neighbours(filename):
    files = [
        f
        for f in listdir(PATH)
        if path.isfile(path.join(PATH, f)) and f.endswith('.jrl')
    ]
    files.sort()

    neighbours = list()  # ['<prev>.jrl', '<next>.jrl']
    file_index = files.index(filename)
    neighbours.append(None if file_index == 0 else files[file_index - 1])
    neighbours.append(
        None if file_index == len(files) - 1 else files[file_index + 1]
    )

    return neighbours

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
    return redirect_dest(fallback=url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
