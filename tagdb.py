#!/usr/bin/env python

# https://docs.python.org/3/library/http.client.html

import sys
import http.client

def usage():
    print("todo: implement usage()")

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    elif sys.argv[1] == 'help':
        usage()
    elif sys.argv[1] == 'list':
        list(sys.argv[2:])
    elif sys.argv[1] == 'tags' and len(sys.argv) == 3:
        tags(sys.argv[-1])
    else:
        usage()
        sys.exit(1)

def list(tags):
    conn = http.client.HTTPConnection('localhost:3134')
    query = '/query?tags=%s' % ','.join(s for s in tags)
    conn.request('GET', query)
    response = conn.getresponse()
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

def tags(obj):
    print('todo: implement tags')

if __name__ == '__main__':
    main()
