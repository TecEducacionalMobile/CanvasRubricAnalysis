# -*- coding: utf-8 -*-
from utils import *
from collections import Counter
from google.appengine.api import users
from secrets import CANVAS
import PIL
import logging
import json
import time
import operator
import urllib
import urllib2
from google.appengine.api import urlfetch


class Assignments(APIHandler):
  
  def get(self):
    course_id = self.request.get('course')
    url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/assignments?per_page=200"
    headers = {'Authorization': CANVAS['AUTH_TOKEN']}
    data = {}
    result = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=60)
    the_page = result.content
    the_page = json.loads(the_page)
    filtered = [i for i in the_page if i.has_key('rubric') == True]

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(filtered))

class Assignment(APIHandler):

  def get(self, *args, **kwargs):
    course_id = kwargs.get('course')
    assignment = kwargs.get('assignment')
    url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/assignments/"+assignment+'/'
    headers = {'Authorization': CANVAS['AUTH_TOKEN']}
    data = {}
    result = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=60)
    the_page = result.content

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(the_page)

class Sections(APIHandler):

  def get(self, *args, **kwargs):
    course_id = kwargs.get('course')
    url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/sections"
    headers = {'Authorization': CANVAS['AUTH_TOKEN']}
    data = {}
    result = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=60)
    the_page = result.content

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(the_page)

class Students(APIHandler):
  def get(self, *args, **kwargs):
    course_id = kwargs.get('course')
    page = 1
    url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/users?page=1&per_page=200"
    headers = {'Authorization': CANVAS['AUTH_TOKEN']}
    data = {}
    result = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=30)
    the_page = result.content
    the_page = json.loads(the_page)
    if len(the_page) >= 99:
      url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/users?page=2&per_page=200"
      headers = {'Authorization': CANVAS['AUTH_TOKEN']}
      data = {}
      result = urlfetch.fetch(url=url,
        method=urlfetch.GET,
        headers=headers,
        deadline=30)
      the_page2 = json.loads(result.content)
      the_page = the_page+the_page2


    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(the_page))

class CompleteSubmissions(APIHandler):
  def get(self, *args, **kwargs):
    course_id = kwargs.get('course')
    assignment = kwargs.get('assignment')
    if(self.request.get('section')):
      url = CANVAS['PROD_ENDPOINT']+"sections/"+str(self.request.get('section'))+"/assignments/"+assignment+"/submissions?include[]=rubric_assessment&per_page=200"
    else:
      url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/assignments/"+assignment+"/submissions?include[]=rubric_assessment&per_page=200"
    headers = {'Authorization': CANVAS['AUTH_TOKEN']}
    data = {}
    result = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=30)
    the_page = result.content
    the_page = json.loads(the_page)
    summary = {}
    students = {}

    url = CANVAS['PROD_ENDPOINT']+"courses/"+course_id+"/assignments/"+assignment+"/"
    result2 = urlfetch.fetch(url=url,
      method=urlfetch.GET,
      headers=headers,
      deadline=30)
    assignment_info = json.loads(result2.content)

    TotalCriteria = {}
    for item in assignment_info['rubric']:
      ratings = set([])
      for rating in item['ratings']:
        ratings.add(rating['points'])
      TotalCriteria[item['id']] = ratings




    pretty_summary = {}
    filtered = [i for i in the_page]
    for student in filtered:
      if 'rubric_assessment' in student:
        for criterium in student['rubric_assessment']:
          if 'points' in  student['rubric_assessment'][criterium]:     
            summary.setdefault(criterium,[]).append(student['rubric_assessment'][criterium]['points'])
            if criterium not in students:
              students[criterium] = {}
            if str(student['rubric_assessment'][criterium]['points']) not in students[criterium]:
              students[criterium][str(student['rubric_assessment'][criterium]['points'])] = []
            students[criterium][str(student['rubric_assessment'][criterium]['points'])].append(student["user_id"])
            TotalCriteria[criterium].discard(student['rubric_assessment'][criterium]['points'])
    totalItemCount = {}
    for item in summary:
      totalItemCount[item] = len(summary[item])
      summary[item] = Counter(summary[item])
    for key in summary:
      array = []
      for element in summary[key]:
        array.append({'rating': element, 'count': (summary[key][element] / float(totalItemCount[key]))*100, 'students': students[key][str(element)]})
      for element in TotalCriteria[key]:
        array.append({'rating': element, 'count': 0, 'students':[]});  
      array.sort(key=operator.itemgetter('rating'), reverse=True)
      pretty_summary[key] = array




    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(pretty_summary))





