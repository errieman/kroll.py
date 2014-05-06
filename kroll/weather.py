"""Weather class to request current weather"""

import requests
import time
import json
import os
import cPickle as pickle

__version__ = '0.4.0'
__author__ = 'Erwin Hager'

class Weather(object):
  """Weather class"""

  def __init__(self, options, apppath):
    self.options = options
    self.pickle_file = apppath
    if self.options.city:
      self.options.force = True

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
    except requests.exceptions.ConnectionError, msg:
      print ('Error connecting to server. '
             'Make sure you are connected to the internet. %s' % msg)
    try:
      data = json.loads(response.text)
    except ValueError, msg:
      print 'Error parsing json data: %s' % msg
    pickle.dump({'lastrequest': time.time(),
        'city': self.GetCity(city),
        'proxy': self.GetProxy(self.options.proxy),
        'weather_data': data}, open(self.pickle_file, 'wb'))
    return data

  def SaveToPickle(self):
    """SaveToPickle"""
    pass

  def WeatherToString(self, weather):
    """Format the weather into a Printable string"""
    self.PrintV('formatting weather')
    return (u"-----------{name}, {sys[country]}-----------\n"
            u"Temperature: {temp} \N{DEGREE SIGN}C "
            u"({main[temp_min]} \N{DEGREE SIGN}C - "
            u"{main[temp_max]} \N{DEGREE SIGN}C)\n"
            u"       Wind: {wind[speed]} Km/h ({wind[deg]}\N{DEGREE SIGN})\n"
            u"   Humidity: {main[humidity]}%\n\n"
            u"Description: {weather[0][description]}"
            ).format(temp=int(weather['main']['temp']),
                **weather)

  def GetCity(self, city):
    """get city"""
    if not city:
      if os.path.exists(self.pickle_file):
        city = pickle.load(open(self.pickle_file, 'rb'))['city']
        if city:
          return city
      print 'No city name provided (use weather -c <city>)'
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
    return 901

  def PrintV(self, msg):
    """verbose messages"""
    if self.options.verbose:\
      print '* ' + msg
