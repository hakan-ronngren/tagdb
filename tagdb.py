#!/usr/bin/env python

# https://docs.python.org/3/library/http.client.html

import sys
import http.client
import urllib.parse

verbose = False

def usage():
    print("usage: tagdb <operation> [<arg> [...]]")
    print("    tagdb tag <tag> [...] <object> : set tag(s) on an object")
    print("    tagdb list <tag> [...]         : list all objects having the given tag(s)")
    print("                                     exclude a tag by prepending it with ^")
    print("    tagdb describe <object>        : list all tags for an object")
    print("    tagdb reload                   : forcefully reload the database")
    print("    tagdb shutdown                 : shut the database down")

def debug(*args):
    if verbose:
        print(*args)

def main():
    global verbose
    switches = [v for v in sys.argv if v.startswith('-')]
    for v in switches:
        if v == '-v':
            verbose = True
        else:
            usage()
            sys.exit(1)

    args = [v for v in sys.argv if not v.startswith('-')]
    if len(args) < 2:
        usage()
        sys.exit(1)
    elif args[1] == 'help':
        usage()
    elif args[1] == 'describe' and len(args) == 3:
        describe(args[-1])
    elif args[1] == 'list':
        list(args[2:])
    elif args[1] == 'tag' and len(args) >= 4:
        tag(args[2:-1], args[-1])
    elif args[1] == 'tags' and len(args) == 2:
        tags()
    elif args[1] == 'reload':
        reload()
    elif args[1] == 'shutdown':
        shutdown()
    else:
        usage()
        sys.exit(1)

def get(query):
    conn = http.client.HTTPConnection('localhost:3134')
    conn.request('GET', query)
    response = conn.getresponse()
    debug(response.status, response.reason)
    if response.status == 200:
        if int(response.getheader('Content-Length')) > 0:
            s = response.getheader('Content-Type')
            i = s.find('charset=')
            if i > 0:
                encoding = s[(i + 8):]
            else:
                encoding = 'utf-8'
            print(response.read().decode(encoding))
    else:
        print(response.reason, file = sys.stderr)
        sys.exit(1)

def list(tags):
    get('/list?tags=%s' % ','.join(s for s in tags))

def describe(obj):
    get('/describe?object=%s' % obj)

def tag(tags, obj):
    conn = http.client.HTTPConnection('localhost:3134')
    params = urllib.parse.urlencode({'object': obj, 'tags': ','.join(tags)})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('PUT', '/tag', params, headers)

def tags():
    get('/tags')

def reload():
    conn = http.client.HTTPConnection('localhost:3134')
    conn.request('POST', '/reload')
    response = conn.getresponse()
    debug(response.status, response.reason)

def shutdown():
    conn = http.client.HTTPConnection('localhost:3134')
    conn.request('POST', '/shutdown')
    response = conn.getresponse()
    debug(response.status, response.reason)

if __name__ == '__main__':
    main()
