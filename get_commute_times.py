# install dependencies
import pandas as pd
import requests
import json
from time import time, sleep
import datetime
from csv import writer

# define time interval for pinging google API (in seconds)
time_interval = 1800

# define origin and destination for commute
origin = 'work'
destination = 'home'
coordinates_origin = '' # add coordinates for the origin of the comute
coordinates_destination = '' # add coordinates for the destination of the commute

print('from ' + origin + ' to ' + destination)

# intialize results file
df = pd.DataFrame(columns = ['time','duration'])
filename = origin + '_to_' + destination + '_' + str(int(time())) + '.csv'
df.to_csv()

# start loop
while(True):
    departure_time = int(time()+70)

# translate departure_time from epoch to human readable and add to vector
    value = datetime.datetime.fromtimestamp(departure_time) - datetime.timedelta(hours=5)
    epoch = value.strftime('%Y-%m-%d %H:%M:%S')

# make URL to access API
    url_components = ["https://maps.googleapis.com/maps/api/distancematrix/json?",
          "origins=",
          coordinates_origin,
          "&destinations=",
          coordinates_destination,
          "&units=imperial",
          "&departure_time=",
          departure_time,
          "&key=XXX"] # replace XXX with personal google API key

    url = "".join(map(str, url_components))

# access google API to get travel time
    payload={}
    headers ={}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.text

# write pulled results to json file
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

# convert json file to python list
    data_python = json.loads(data)
    duration = data_python['rows'][0]['elements'][0]['duration_in_traffic']['text']

    print(epoch)
    print(duration)

# write results to file
    new_results = [epoch, duration]

    with open(filename, 'a', newline='') as f_object:
      writer_object = writer(f_object)
      writer_object.writerow(new_results)
      f_object.close()

    sleep(time_interval)
