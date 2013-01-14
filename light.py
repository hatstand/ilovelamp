#!/usr/bin/python

import json
import random
import requests
import time

KEY = '1135e33d2a71c68723e314f913ace2a3'
URL = 'http://192.168.0.168/api/%s/lights/%d'

class LampError(Exception):
  pass


class LampApiError(LampError):
  def __init__(self, error):
    self.error = error
    super(LampError, self).__init__('%s (error code %d)' % (
        self.error['description'], self.error['type']))


class ILoveLamp(object):
  RO_PROPERTIES = ('type', 'name', 'modelid', 'swversion')
  RW_STATE = set(['on', 'bri', 'hue', 'sat', 'xy', 'ct', 'alert', 'effect',
                  'colormode'])

  def __init__(self, lamp_number):
    self.url = URL % (KEY, lamp_number)
    self.state_url = self.url + '/state'
    self.update()

  def update(self):
    data = requests.get(self.url).json()
    print data

    for key in self.RO_PROPERTIES:
      setattr(self, key, data[key])

    for key in self.RW_STATE:
      setattr(self, key, data['state'][key])

  def set(self, **kwargs):
    for key in kwargs:
      if key not in self.RW_STATE:
        raise LampError('Unknown key %s' % key)

    response = requests.put(self.state_url, data=json.dumps(kwargs)).json()
    print response
    if 'error' in response[0]:
      raise LampApiError(response[0]['error'])

    for key, value in kwargs.items():
      setattr(self, key, value)


def main():
  lamps = [ILoveLamp(x+1) for x in xrange(3)]

  while True:
    for i, lamp in enumerate(lamps):
      lamp.set(sat=254, hue=random.randint(0, 65535), on=True)
    time.sleep(1)

if __name__ == '__main__':
  main()

