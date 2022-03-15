from . import app
from .decryption import get_decrypt_func
from .config_parser import ConfigParser
from flask import (  # type: ignore
    render_template, request, session, url_for, redirect, abort
)
from flask import __version__ as flask_version
from typing import Callable
import random
import os
import re
import sys

def get_handles():
    return ConfigParser('config').get_instances()

@app.errorhandler(404)
def page_not_found(_):
    try:
        with open('404.txt') as missings_file:
            possible_missings = missings_file.readlines()

        # removes whitespace characters like `\n` at the end of each line
        possible_missings = [ m.strip() for m in possible_missings ]

    except FileNotFoundError:
        possible_missings = 'File'

    return render_template('404.html',
        missing=random.choice(possible_missings),
    ), 404

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
    files = sorted(get_files(path, extension))

    neighbours = list()  # ['<prev>.jrl', '<next>.jrl']
    file_index = files.index(filename)
    neighbours.append(None if file_index == 0              else files[file_index - 1])
    neighbours.append(None if file_index == len(files) - 1 else files[file_index + 1])

    return neighbours

@app.route("/")
def index():
    menu = dict()

    # Generate a decrypt function
    key: Optional[str] = get_key()
    decrypt_func: Optional[Callable[[str], str]] = \
        get_decrypt_func(key) if key is not None else None

    # Prepare menu
    for handle in get_handles():
        cat = handle.get_category()
        menu[cat] = dict()

        for file in sorted(get_files(handle.get_path(), handle.get_extension()), reverse=True):
            handle.set_filename(handle.get_path() + os.sep + file)
            handle.read_file(decrypt=decrypt_func)
            handle.parse()
            menu[cat][file] = handle.get_title()

    return render_template('index.html',
        menu=menu,
        key_exists=(get_key() is not None),
    )

@app.route("/<filename>")
def render_article(filename):
    handler = None

    for handle in get_handles():
        if filename.endswith(handle.extension):
            handler = handle
            break

    if not handler:
        abort(404)

    file_path = handler.get_path()
    if not file_path.endswith(os.sep):
        file_path += os.sep
    file_path += filename

    if not os.path.exists(file_path):
        abort(404)

    handler.set_filename(file_path)

    key: Optional[str] = get_key()
    handler.read_file(
        decrypt=get_decrypt_func(key) if key is not None else None
    )

    handler.parse()
    handler.to_html()

    prev, next = get_neighbours(filename, handler.get_path(), handle.get_extension())

    return render_template("article.html",
        filename=handler.get_filename(),
        title=handler.get_title(),
        body=handler.get_html_paragraphs(),
        date=handler.get_date('%B %d, %Y -- %A'),
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
    return render_template('about.html',
        server=request.environ.get('SERVER_SOFTWARE'),
        os_uname=os.uname(),
        py_version=sys.version,
        py_releaselevel=sys.version_info.releaselevel,
        flask_version=flask_version,
    )
