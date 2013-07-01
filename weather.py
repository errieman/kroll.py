#!/usr/bin/python
"""
get the current weather information at your location.
the data will only be fetched 15 minutes after the last call, before
that the data will be read from local storage. (use -f to override this)
"""

__version__ = '0.9.13'
__author__ = 'Erwin Hager <errieman@gmail.com>'

import argparse
import requests
import time
import json
import sys
import os
import cPickle as pickle

class Weather:
  """Weather class"""

  def __init__(self, options):
    self.options = options
    self.pickle_file = os.path.join(self.GetAppPath(), "weather.pickle")

  def GetWeather(self):
    """return weather as string"""    
    self.PrintV('Last request %d minutes ago' %
        round((time.time() - self.GetLastTime()) / 60))
    if time.time() - self.GetLastTime() >= 900 or self.options.force:
      self.PrintV('making new request')
      weather = self.FetchWeather(proxy=self.GetProxy(self.options.proxy),
        city=self.options.city)
    else:
      self.PrintV('no need for new request')
      weather = pickle.load(open(self.pickle_file, 'rb'))['weather_data']
    return self.WeatherToString(weather) if not self.options.raw else weather

  def FetchWeather(self, proxy='', city=''):
    """Fetch weather from api server"""
    self.PrintV('fetching weather')    
    try:
      self.PrintV('using proxy: %s' % proxy)
      response = requests.get(('http://api.openweathermap.org/data/2.5/weather?'
                             'q=%s&'
                             'units=metric&'
                             'APPID=5bfe42c795bc9f9598fce303e7aee224') %
                              self.GetCity(city),
                   proxies={'http': proxy})
      data = json.loads(response.text)
      pickle.dump({'lastrequest': time.time(),
          'city': self.GetCity(city),
          'proxy': proxy,
          'weather_data': data}, open(self.pickle_file, 'wb'))
      return data
    except requests.exceptions.ConnectionError:
      print('Error connecting to server')
      exit(0)

  def WeatherToString(self, weather):
    """Format the weather into a Printable string"""
    self.PrintV('formatting weather')
    return (u"Temperature: {main[temp]} \u00b0C ({main[temp_min]} \u00b0C - "
            u"{main[temp_max]} \u00b0C)\n"
            u"       Wind: {wind[speed]} Km/h ({wind[deg]}\u00b0)\n"
            u"   Humidity: {main[humidity]}%\n\n"
            u"Description: {weather[0][description]}"
            ).encode('utf8').format(**weather)

  def GetCity(self, city):
    """get city"""    
    if not city:
      if os.path.exists(self.pickle_file):
        city = pickle.load(open(self.pickle_file, 'rb'))['city']
        if city:
          return city
      print('No city name provided (use weather -c <city>)')
      exit(0)
    else:
      return city

  def GetProxy(self, proxy):
    """Get saved proxy address"""    
    if not proxy and not proxy == 'none':
      if os.path.exists(self.pickle_file):
        proxy = pickle.load(open(self.pickle_file, 'rb'))['proxy']
        if proxy and not proxy == 'none':
          return proxy
        return None
    else:
      return None
    return proxy


  def GetLastTime(self):
    """Last request time"""    
    if os.path.exists(self.pickle_file):
      return pickle.load(open(self.pickle_file, 'rb'))['lastrequest']
    else:
      return 1000

  def PrintV(self, msg):
    """verbose messages"""
    if self.options.verbose:
      print('* ' + msg)

  def GetAppPath(self):
    """get application path"""
    if getattr(sys, 'frozen', False):
      return os.path.dirname(sys.executable)
    elif __file__:
      return os.path.dirname(__file__)

def main():
  """Main method"""
  optp = argparse.ArgumentParser(description='Display local weather data.',
      epilog=__doc__)
  optp.add_argument('-c', '--city', 
      help='Set city name (only needs to be set once)')
  optp.add_argument('-v', '--verbose', action='store_true',
      help='Enable verbose mode.')
  optp.add_argument('-f', '--force', action='store_true',
      help='Force new request.')
  optp.add_argument('-p', '--proxy', default='',
      help='Set proxy address (only needs to be set once) '
           'use none to disable proxy.')
  optp.add_argument('-r', '--raw', action='store_true',
      help='Display raw data.')
  options = optp.parse_args()
  weather = Weather(options)
  print weather.GetWeather()

if __name__ == '__main__':
  main()
