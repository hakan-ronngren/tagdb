#!/usr/bin/env python

from flask import Flask
from flask import request

import glob, os, sys

CONFIG_FILE = 'tagdb-config.yaml'

app = Flask(__name__)

def load_database():
    global db
    db = {}
    for f in glob.glob('*.tag'):
        with open(f) as io:
            db[f.split('.')[0]] = {line.strip() for line in io.readlines()}

@app.route('/query', methods = ['GET'])
def query():
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
