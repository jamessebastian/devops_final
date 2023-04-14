import time

import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return ' <a href="/">1st page</a><a href="/1">2nd page</a><a href="/2">3rd page</a> hit-- {} times.\n'.format(count)

@app.route('/1')
def hello1():
    count = get_hit_count()
    return ' <a href="/">1st page</a><a href="/1">2nd page</a><a href="/2">3rd page</a> hit-- {} times.\n'.format(count)

@app.route('/2')
def hello2():
    count = get_hit_count()
    return ' <a href="/">1st page</a><a href="/1">2nd page</a><a href="/2">3rd page</a> hit-- {} times.\n'.format(count)


@app.route('/page1')
def index():
    return render_template('index.html')

@app.route('/page2')
def page1():
    return render_template('page1.html')

@app.route('/page3')
def page2():
    return render_template('page2.html')