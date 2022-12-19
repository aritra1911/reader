from . import app
from .decryption import get_decrypt_func
from .config_parser import ConfigParser
from .article import Article, FileParsingError
from flask import (
    render_template, request, session, url_for, redirect, abort
)
from flask import __version__ as flask_version
from typing import List, Optional
import random
import fnmatch
import os
import re
import sys

PREFIX = '/home/aritra/pgm/reader/flask/'

FILE_PATH = {
    'config': PREFIX + 'config',
    '404.txt': PREFIX + '404.txt',
}

def get_config() -> ConfigParser:
    return ConfigParser(FILE_PATH['config'])

@app.errorhandler(404)
def page_not_found(_):
    try:
        with open(FILE_PATH['404.txt']) as missings_file:
            possible_missings = missings_file.readlines()

        # removes whitespace characters like `\n` at the end of each line
        possible_missings = [ m.strip() for m in possible_missings ]

    except FileNotFoundError:
        possible_missings = 'File'

    return render_template('404.html',
        missing=random.choice(possible_missings),
    ), 404

def get_key() -> Optional[str]:
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

def get_neighbours(filename: str, category: str):
    config = get_config()
    files = sorted(config.get_files(category))

    neighbours = list()  # ['<prev>.jrl', '<next>.jrl']
    file_index = files.index(filename)
    neighbours.append(None if not file_index else files[file_index - 1])
    neighbours.append(None if file_index == len(files) - 1
                           else files[file_index + 1])

    return neighbours

@app.route("/")
def index():
    menu = dict()
    config = get_config()

    # Generate a decrypt function
    key = get_key()
    decrypt_func = get_decrypt_func(key) if key else None

    # Prepare menu
    for cat in config.get_categories():
        menu[cat] = dict()

        for file in sorted(config.get_files(cat), reverse=True):
            handle = Article(
                config.get_path(cat) + os.sep + file,
                skipbody=True
            )
            handle.read_file(decrypt=decrypt_func)
            try:
                handle.parse()
            except FileParsingError:
                menu[cat][file] = ['<Empty File!>']
                continue
            menu[cat][file] = handle.get_title()

    return render_template('index.html',
        menu=menu,
        key_exists=(get_key() is not None),
    )

@app.route("/<filename>")
def render_article(filename):
    config = get_config()

    cat = config.get_category_from_filename(filename)
    if not cat:
        abort(404);

    file_path = os.path.join(config.get_path(cat), filename)
    if not os.path.exists(file_path):
        abort(404)

    handler = Article(file_path)

    key: Optional[str] = get_key()
    handler.read_file(decrypt=get_decrypt_func(key) if key else None)

    handler.parse()
    handler.to_html()

    prev, next = get_neighbours(filename, cat)

    return render_template("article.html",
        filename=filename,
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
        if key: session['key'] = key

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
