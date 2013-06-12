#!/usr/bin/python
appinfo = """
WEERHOOFDEN
-------------------------------------------------------------------------------
get the current weather information at your location

author: Erwin Hager <errieman@gmail.com>
version: 0.9.6

--- Usage ---

weather [ -f | -v | -l <city> ]

  -f  force new request.
  -v  verbose mode.
  -l  city name ( weather -l Leeuwarden ).
      The city name only has to be set once.

New data will be fetched every 15 minutes, before that the data will be read
from local storage. (use -f to override this)
"""

import requests
import time
import json
import sys
import os

import cPickle as pickle

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

cargs = sys.argv
r_proxies =  {}
make_request = False
verbose = False
pickle_file = os.path.join(application_path, "weather.pickle")
weather = ''
city = ''

def log(message):
  if verbose:
    print '* ' + message

if '-h' in cargs:
  print appinfo
  exit(0)
if '-l' in cargs:
  city = cargs[cargs.index('-l') + 1]
  make_request = True
if '-v' in cargs:
  verbose = True
  log('verbose mode enabled')
if '-f' in cargs:
  make_request = True
  log('will force request')
if '-p' in cargs:
  r_proxies = {'http': 'http://%s/' % cargs[cargs.index('-p') + 1]}
  log('set proxy to ' + cargs[cargs.index('-p') + 1])
if not os.path.exists(pickle_file):
  log('pickle file not present')
  thefile = open(pickle_file, 'wb')
  pickle.dump({"lastrequest": -1, "city": city, "weather_data": {} }, thefile)
  thefile.close()
try:
  thefile = open(pickle_file, 'rb')
  data = pickle.load(thefile)
  if data['city'] == '' and city == '':
    log('no city provided, guessing location')
  elif city == '':
    city = data['city']
  log("%d minutes since last request (%s)" % ((time.time() - data['lastrequest']) / 60, time.ctime(data['lastrequest'])))
  if time.time() - data['lastrequest'] >= 900:
    log('I\'ve waited long enough')
    make_request = True
    thefile.close()
except Exception, e:
  log('error, making request anyway just to be sure (' + str(e) + ')')
  make_request = True


if make_request:
  log('making new request for some reason')
  r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&APPID=5bfe42c795bc9f9598fce303e7aee224' % city,
                   proxies=r_proxies)

  weather = json.loads(r.text)

  pickle_data = { "lastrequest": time.time(), "city": city, "weather_data": weather }
  thefile = open(pickle_file, 'wb')
  pickle.dump(pickle_data, thefile)
else:
  log('reading weather data from local storage')
  thefile = open(pickle_file, 'rb')
  weather = pickle.load(thefile)['weather_data']
  thefile.close()

printweather = u"""temp: {main[temp]} \u00b0C ({main[temp_min]} \u00b0C - {main[temp_max]} \u00b0C)
wind: {wind[speed]} Km/h ({wind[deg]} \u00b0)
humidity: {main[humidity]}%

description: {weather[0][description]}""".encode('utf8').format(**weather)

print printweather if not '--raw' in cargs else weather

exit(0)
