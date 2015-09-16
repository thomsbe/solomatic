import json
import urllib2

from solongo.rmqtools import publish
from solongo.types import MsgClima

response = urllib2.urlopen('http://officepi.solongo.office:8083/fhem?cmd=jsonlist2%20netatmo_office&XHR=1')
data = json.loads(response)
temp = data['Results'][0]['Readings']['temperature']['Value']
hum = data['Results'][0]['Readings']['humidity']['Value']

temperature = MsgClima(temp, hum)
message = json.dumps(temperature, default=lambda o: o.__dict__)

publish(message)