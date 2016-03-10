# -*- coding: utf-8 -*-

import os
import re
import random
import hashlib
import urllib
import hmac
import logging
from string import letters

import webapp2
import jinja2
import logging
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

secret = "mysecret"


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def logged(self):
        return True if self.read_secure_cookie('logged') == 'YES' else False

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        logging.error(str(type(val)) + ' ' + val)
        cookie_val = make_secure_val(val)
        self.response.set_cookie(name, cookie_val)

    def set_inexpirable_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; expires=Fri, 01-Jan-2112 23:59:59 GMT; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def initialize(self, *a, **kw): 
        webapp2.RequestHandler.initialize(self, *a, **kw)
        if self.read_secure_cookie('logged') == 'YES':
            self.user = { 'name' : self.read_secure_cookie('name')}
        else:
            self.user = None
class APIHandler(Handler):
    def dispatch(self):
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Authorization" 
            self.response.headers['Access-Control-Allow-Methods'] = 'GET,POST, OPTIONS'
            super(APIHandler, self).dispatch()
    def options(self):
        self.response.out.write('ok')







