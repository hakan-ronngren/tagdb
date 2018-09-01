#!/usr/bin/env python

from flask import Flask
from flask import request

import glob, os, sys, yaml

CONFIG_FILE = 'tagdb-config.yaml'

app = Flask(__name__)

def load_database():
    global db
    db = {}
    for f in glob.glob('*.tag'):
        with open(f) as io:
            db[f.split('.')[0]] = {line.strip() for line in io.readlines()}

@app.route('/list', methods = ['GET'])
def list():
    global db
    taglist = request.args.get('tags')
    if taglist is None:
        return ''
    else:
        tags = taglist.split(',')
        matches = db.get(tags.pop(), set())
        for tag in tags:
            matches = matches.intersection(db.get(tag, {}))
        return '\n'.join(m for m in matches)

@app.route('/describe', methods = ['GET'])
def describe():
    global db
    obj = request.args.get('object')
    if obj is None:
        return ''
    else:
        tags = [tag for tag in db.keys() if obj in db[tag]]
        return '\n'.join(tags)

# Chosen to always use PUT to assign a tag, as the operation is required to be
# idempotent, which is not generally what you expect POST operations to be.
@app.route('/tag', methods = ['PUT'])
def tag():
    global db
    obj = request.form['object']
    tags = request.form['tags'].split(',')
    for tag in tags:
        objs = db.get(tag, set())
        objs.add(obj)
        db[tag] = objs
        with open(tag + '.tag', 'w') as f:
            f.write(''.join(["%s\n" % obj for obj in db[tag]]))
    return ''

@app.route('/tags', methods = ['GET'])
def tags():
    global db
    keys = []
    for k in db.keys():
        keys.append(k)
    keys.sort()
    return '\n'.join(keys)

@app.route('/reload', methods = ['POST'])
def reload():
    load_database()
    return ''

@app.route('/shutdown', methods = ['POST'])
def shutdown():
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
