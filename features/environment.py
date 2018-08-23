import http.client
import glob, os, time

def before_all(context):
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
