from requests import get
import matplotlib.pyplot as plt
from dateutil import parser

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallmeasurements/3528546'

weather = get(url).json()

temperatures = []

for record in weather['items']:
    temperature = record['ambient_temp']
    temperatures.append(temperature)

# OR:
# temperatures = [record['ambient_temp'] for record in weather['items']]

timestamps = [parser.parse(record['reading_timestamp']) for record in weather['items']]

plt.plot(timestamps, temperatures)
plt.ylabel('Temperature')
plt.xlabel('Time')
plt.title('Test Temp vs Time plot')
plt.show()
