#!/usr/bin/env python

# https://docs.python.org/3/library/http.client.html

import sys
import http.client
import urllib.parse

verbose = False

def usage():
    print("todo: implement usage()")

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
    elif args[1] == 'list':
        list(args[2:])
    elif args[1] == 'tag' and len(args) >= 4:
        tag(args[2:-1], args[-1])
    #elif args[1] == 'tags' and len(args) == 3:
    #    tags(args[-1])
    else:
        usage()
        sys.exit(1)

def list(tags):
    conn = http.client.HTTPConnection('localhost:3134')
    query = '/list?tags=%s' % ','.join(s for s in tags)
    conn.request('GET', query)
    response = conn.getresponse()
    if verbose:
        print(response.status, response.reason)
    if response.status == 200:
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

def tag(tags, obj):
    global verbose
    conn = http.client.HTTPConnection('localhost:3134')
    params = urllib.parse.urlencode({'object': obj, 'tags': ','.join(tags)})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('PUT', '/tag', params, headers)
    response = conn.getresponse()
    debug(response.status, response.reason)

def tags(obj):
    print('todo: implement tags')

if __name__ == '__main__':
    main()
