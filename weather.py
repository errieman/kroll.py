#!/usr/bin/python
"""
WEERHOOFDEN
-------------------------------------------------------------------------------
get the current weather information at your location

author: Erwin Hager <errieman@gmail.com>
version: 0.9.11

--- Usage ---

weather [ -f | -v | -c <city> ]

  -f, --force    force new request.
  -v, --verbose  verbose mode.
  -c, --city     city name ( weather -l Leeuwarden ).
                 The city name only needs to be set once.
  -p, --proxy    set HTTP Proxy if using one.

New data will only be fetched 15 minutes after the last call, before
that the data will be read from local storage. (use -f to override this)
"""

__version__ = '0.9.11'
__author__ = 'Erwin Hager <errieman@gmail.com>'

import requests
import time
import json
import sys
import os
import cPickle as pickle

from optparse import OptionParser

VERBOSE = False

def main():
  """Main method"""
  optp = OptionParser(add_help_option=False)
  optp.add_option('-c', '--city')
  optp.add_option('-v', '--verbose', action='store_true')
  optp.add_option('-f', '--force', action='store_true')
  optp.add_option('-p', '--proxy')
  optp.add_option('-r', '--raw', action='store_true')
  optp.add_option('-h', '--help', action='store_true')
  (options, args) = optp.parse_args()
  global VERBOSE
  VERBOSE = options.verbose
  if options.help:
    print __doc__
    return
  print GetWeather(options)

def GetWeather(options):
  """return weather as string"""
  pickle_file = os.path.join(GetAppPath(), "weather.pickle")
  PrintV('Last request %d minutes ago' %
      round((time.time() - GetLastTime()) / 60))
  if time.time() - GetLastTime() >= 900 or options.force:
    PrintV('making new request')
    weather = FetchWeather(proxy=GetProxy(options.proxy), city=options.city)
  else:
    PrintV('no need for new request')
    weather = pickle.load(open(pickle_file, 'rb'))['weather_data']
  return WeatherToString(weather) if not options.raw else weather

def FetchWeather(proxy='', city=''):
  """Fetch weather from api server"""
  PrintV('fetching weather')
  pickle_file = os.path.join(GetAppPath(), "weather.pickle")
  try:
    response = requests.get(('http://api.openweathermap.org/data/2.5/weather?'
                           'q=%s&'
                           'units=metric&'
                           'APPID=5bfe42c795bc9f9598fce303e7aee224') %
                            GetCity(city),
                 proxies={'http': proxy})
    data = json.loads(response.text)
    pickle.dump({'lastrequest': time.time(),
        'city': GetCity(city),
        'proxy': proxy,
        'weather_data': data}, open(pickle_file, 'wb'))
    return data
  except requests.exceptions.ConnectionError:
    print('Error connecting to server')
    exit(0)

def WeatherToString(weather):
  """Format the weather into a Printable string"""
  PrintV('formatting weather')
  return (u"Temperature: {main[temp]} \u00b0C ({main[temp_min]} \u00b0C - "
          u"{main[temp_max]} \u00b0C)\n"
          u"       Wind: {wind[speed]} Km/h ({wind[deg]}\u00b0)\n"
          u"   Humidity: {main[humidity]}%\n\n"
          u"Description: {weather[0][description]}"
          ).encode('utf8').format(**weather)

def GetCity(city):
  """get city"""
  pickle_file = os.path.join(GetAppPath(), "weather.pickle")
  if not city:
    if os.path.exists(pickle_file):
      city = pickle.load(open(pickle_file, 'rb'))['city']
      PrintV('city = %s' % city)
      if city:
        return city
    print('No city name provided (use weather -c <city>)')
    exit(0)
  else:
    return city

def GetProxy(proxy):
  """Get saved proxy address"""
  pickle_file = os.path.join(GetAppPath(), "weather.pickle")
  if proxy == '':
    if os.path.exists(pickle_file):
      proxy = pickle.load(open(pickle_file, 'rb'))['proxy']
      PrintV('proxy = %s' % proxy)
      if proxy:
        return proxy
  else:
    return proxy


def GetLastTime():
  """Last request time"""
  pickle_file = os.path.join(GetAppPath(), "weather.pickle")
  if os.path.exists(pickle_file):
    return pickle.load(open(pickle_file, 'rb'))['lastrequest']
  else:
    return 1000

def PrintV(msg):
  """verbose messages"""
  if VERBOSE:
    print('* ' + msg)

def GetAppPath():
  """get application path"""
  if getattr(sys, 'frozen', False):
    return os.path.dirname(sys.executable)
  elif __file__:
    return os.path.dirname(__file__)

if __name__ == '__main__':
  main()

