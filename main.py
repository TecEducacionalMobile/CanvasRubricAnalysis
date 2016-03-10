#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import webapp2
import logging
import re
from Handlers import Home
from Handlers import utils

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Render HTML with resource error')
    response.set_status(404)

app = webapp2.WSGIApplication([
							   webapp2.Route(r'/api/assignments',Home.Assignments),
							   webapp2.Route(r'/api/students/<course>',Home.Students),
							   webapp2.Route(r'/api/sections/<course>',Home.Sections),
							   webapp2.Route(r'/api/assignments/<course>/<assignment>', Home.Assignment),
							   webapp2.Route(r'/api/assignments/<course>/<assignment>/submissions', Home.CompleteSubmissions)], debug=True)

app.error_handlers[404] = handle_404
