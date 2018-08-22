import glob, os, time

def after_scenario(context, scenario):
    os.system('pkill -f tagdb-server.py')
    for f in glob.glob('features/testdata/*.tag'):
        os.remove(f)
