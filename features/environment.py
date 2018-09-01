import http.client
import glob, os, time

def before_all(context):
    # If there is a server on this port, shut it down
    try:
        http.client.HTTPConnection('localhost:3134').request('POST', '/shutdown')
        while True:
            try:
                http.client.HTTPConnection('localhost:3134').request('GET', '/')
                time.sleep(0.1)
            except ConnectionRefusedError as e:
                break
    except ConnectionRefusedError as e:
        pass

    # Start a server in the test data directory
    os.system('cd features/testdata && ( ../../tagdb-server.py > testserver.log 2>&1 & ) &')
    while True:
        try:
            http.client.HTTPConnection('localhost:3134').request('GET', '/')
            return
        except ConnectionRefusedError as e:
            time.sleep(0.1)

def before_scenario(context, scenario):
    http.client.HTTPConnection('localhost:3134').request('POST', '/reload')

def after_scenario(context, scenario):
    for f in glob.glob('features/testdata/*.tag'):
        os.remove(f)

def after_all(context):
    http.client.HTTPConnection('localhost:3134').request('POST', '/shutdown')
