#!/usr/bin/env python

from flask import Flask
from flask import request

import glob, os, sys, yaml

CONFIG_FILE = 'tagdb-config.yaml'
ALL_SYMBOL = '*'

app = Flask(__name__)

def load_database():
    global db
    db = {}
    db[ALL_SYMBOL] = set()
    for f in glob.glob('*.tag'):
        tag = f.split('.')[0]
        with open(f) as io:
            db[tag] = {line.strip() for line in io.readlines()}
            db[ALL_SYMBOL] = db[ALL_SYMBOL].union(db[tag])

def all_tags():
    global db
    tags = list(set(db.keys()).difference({ALL_SYMBOL}))
    tags.sort()
    return tags

@app.route('/list', methods = ['GET'])
def serve_list():
    global db
    taglist = request.args.get('tags')
    if taglist is None:
        return ''
    else:
        matches = db[ALL_SYMBOL]
        tags = taglist.split(',')
        for tag in tags:
            if tag.startswith('^'):
                matches = matches.difference(db.get(tag[1:], {}))
            else:
                matches = matches.intersection(db.get(tag, {}))
        return '\n'.join(m for m in matches)

@app.route('/describe', methods = ['GET'])
def serve_describe():
    global db
    obj = request.args.get('object')
    if obj is None:
        return ''
    else:
        tags = [tag for tag in all_tags() if obj in db[tag]]
        return '\n'.join(tags)

# Chosen to always use PUT to assign a tag, as the operation is required to be
# idempotent, which is not generally what you expect POST operations to be.
@app.route('/tag', methods = ['PUT'])
def serve_tag():
    global db
    obj = request.form['object']
    tags = request.form['tags'].split(',')
    for tag in tags:
        # update the set for all
        objs = db.get(ALL_SYMBOL, set())
        objs.add(obj)
        db[ALL_SYMBOL] = objs
        # update and persist the set for the tag
        objs = db.get(tag, set())
        objs.add(obj)
        db[tag] = objs
        with open(tag + '.tag', 'a') as f:
            f.write('%s\n' % obj)
    return ''

@app.route('/tags', methods = ['GET'])
def serve_tags():
    return '\n'.join(all_tags())

@app.route('/reload', methods = ['POST'])
def serve_reload():
    load_database()
    return ''

@app.route('/shutdown', methods = ['POST'])
def serve_shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'shutting down...'

if __name__ == '__main__':
    load_database()
    try:
        with open(CONFIG_FILE) as f:
            config = yaml.load(''.join(f.readlines()))
    except FileNotFoundError:
        print('no %s here - using defaults' % CONFIG_FILE)
        config = {'port': 3134}
    app.run(host = '127.0.0.1', threaded = False, debug = True, port = config['port'])
