from behave import *
import os, time
import sure
import http.client

@given('that the tag "{tag}" applies to "{objects}"')
def step_impl(context, objects, tag):
    with open('features/testdata/%s.tag' % tag, 'w') as f:
        for object in objects.split(','):
            f.write(object + '\n')

@given('the daemon is running')
def step_impl(context):
    os.system('mkdir -p features/testdata && cd features/testdata && ( ../../tagdb-server.py > /dev/null 2>&1 & ) &')
    while True:
        try:
            http.client.HTTPConnection('localhost:3134').request('GET', '/')
            return
        except ConnectionRefusedError as e:
            time.sleep(0.1)

@when('I issue: "{commandline}"')
def step_impl(context, commandline):
    global output
    output = os.popen('./' + commandline).read()

@then('the output lines should be "{expected}" in any order')
def step_impl(context, expected):
    global output
    expected_set = set(expected.split(','))
    output_set = set(output.strip().split('\n'))
    output_set.should.equal(expected_set)

@then('the output should be empty')
def step_impl(context):
    global output
    output.should.equal('\n')
