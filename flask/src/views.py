from . import app
from .article import Journal, Story, Idea
from .decryption import get_decrypt_func
from flask import render_template, request, session, url_for, redirect
#from os import environ, sep, listdir, path
import os
import re

handles = [
    Journal(os.environ['JOURNALS_DIR']),
    Story(os.environ['STORIES_DIR']),
    Idea(os.environ['IDEAS_DIR']),
]

def get_files(path, extension):
    return [
        f
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f)) and f.endswith(extension)
    ]

def get_key():
    try:
        return session['key']
    except KeyError:
        return None

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

def get_neighbours(filename, path, extension):
    files = get_files(path, extension).sort()

    neighbours = list()  # ['<prev>.jrl', '<next>.jrl']
    file_index = files.index(filename)
    neighbours.append(None if file_index == 0 else files[file_index - 1])
    neighbours.append(
        None if file_index == len(files) - 1 else files[file_index + 1]
    )

    return neighbours

@app.route("/")
def index():
    menu = {
        "Journal Entries": {
            "instance": JournalEntry(),
            "path": environ['JOURNALS_DIR'],
            "files": dict(),
        },
        "Stories": {
            "instance": Story(),
            "path": environ['STORIES_DIR'],
            "files": dict(),
        },
        "Ideas": {
            "instance": Idea(),
            "path": environ['IDEAS_DIR'],
            "files": dict(),
        },
    }

    # Generate a decrypt function
    decrypt_func = get_decrypt_func(get_key())

    # Populate `files` dicts
    for key, value in menu.items():
        for file in sorted(get_files(value["path"], value["instance"].get_extension()), reverse=True):
            value["instance"].set_filename(value["path"] + sep + file)
            value["instance"].read_file(decrypt=decrypt_func)
            value["instance"].parse()
            value["files"][file] = value["instance"].get_title()

    return render_template('index.html',
        menu=menu,
        key_exists=(get_key() is not None),
    )

@app.route("/<filename>")
def render_journal(filename):
    entry = JournalEntry()
    entry.set_filename(PATH + os.sep + filename)
    entry.read_file(decrypt=get_decrypt_func(get_key()))
    entry.parse()
    entry.to_html()

    prev, next = get_neighbours(filename)

    return render_template("journal.html",
        filename=entry.get_filename(),
        title=entry.get_title(),
        body=entry.get_html_paragraphs(),
        date=entry.get_date('%B %d, %Y -- %A'),
        key_exists=(get_key() is not None),
        prev=prev,
        next=next,
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
    return redirect_dest(fallback=url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
