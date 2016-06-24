#!/usr/bin/env python
# -*- coding: utf-8 -*- 

config = {
    'latituide': '52.5',
    'longitude': '13.3',
    'api': 'http://w.shtr.eu/'
}

import urllib2, json

def fetch(url):
    req = urllib2.Request(url)
    response=urllib2.urlopen(req)
    return response.read()

def getJSON():
	return json.loads(fetch(config['api'] + "?lat=" + config['latituide']+"&lon=" + config['longitude']))

def main():
	jData = getJSON()

	print "Weather: " + str(jData['current']['weather'][0]['main'])
	print "Temperature: " + str(int(jData['current']['main']['temp'])) + " " + u'\xB0' + "C"
	print "Pressure: " + str(int(jData['current']['main']['pressure'])) + " hPa"
	print "Humidity: " + str(int(jData['current']['main']['humidity'])) + " %"
	print "Wind: " + str(int(jData['current']['wind']['speed'])) + " m/s"

if __name__ == "__main__":
	main()