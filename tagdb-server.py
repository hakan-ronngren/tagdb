#!/usr/bin/env python

from flask import Flask
from flask import request

import glob, os

app = Flask(__name__)

db = {}
for f in glob.glob('*.tag'):
    with open(f) as io:
        db[f.split('.')[0]] = {line.strip() for line in io.readlines()}

@app.route('/query')
def display():
    taglist = request.args.get('tags')
    if taglist is None:
        return ''
    else:
        tags = taglist.split(',')
        matches = db.get(tags.pop(), set())
        for tag in tags:
            matches = matches.intersection(db.get(tag, {}))
        return '\n'.join(m for m in matches)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', threaded=False, debug=True, port=3134)
