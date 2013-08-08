#!/usr/bin/python
"""
get the current weather information at your location.
the data will only be fetched 15 minutes after the last call, before
that the data will be read from local storage. (use -f to override this)
"""

import argparse

import sys
import os

from . import forecast, weather
from os.path import expanduser

__version__ = '0.3.46'

# def GetAppPath():
#   """get application path"""
#   if getattr(sys, 'frozen', False) and not __file__:
#     return os.path.dirname(sys.executable)
#   return os.path.dirname(__file__)

def main():
  """Main method"""
  optp = argparse.ArgumentParser(description='Display local weather data.',
      epilog=__doc__)
  optp.add_argument('-s', '--predict', action='store_true',
      help='show weather forecast information')
  optp.add_argument('-c', '--city',
      help='set city name (only needs to be set once)')
  optp.add_argument('-v', '--verbose', action='store_true',
      help='enable verbose mode.')
  optp.add_argument('-f', '--force', action='store_true',
      help='force new request.')
  optp.add_argument('-p', '--proxy', default='',
      help='set proxy address (only needs to be set once) '
           'use "none" to disable proxy.')
  optp.add_argument('-r', '--raw', action='store_true',
      help='display raw data.')
  options = optp.parse_args()
  if options.predict:
    weath = forecast.Forecast(options)
  else:
    weath = weather.Weather(options,
        os.path.join(expanduser("~"), "weather.pickle"))
  print weath.GetWeather()

if __name__ == '__main__':
  main()
