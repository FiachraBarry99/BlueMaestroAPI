# BlueMaestroAPI
#### An unofficial Python API for interacting with Blue Maestro's sensors.  

I wrote this for a project I was working on and figured I would share it as there is no official Blue Maestro API for desktop. Currently, it is just a Python module but I can package it up and make it available on pypi if there's interest. To use this API just download the BlueMaestroAPI.py file and place it in the directory you are working in.  

## How it Works
The API uses the [Bleak](https://github.com/hbldh/bleak) library to scan for advertising data packets and checks if they're Blue Maestro packets using the manufacturing number. If Blue Maestro packets are detected it will return them as a list of packets in their raw little endian encoded structure. The first element in the list will be the first packet according to the Blue Maestro guide which can be found [here](https://usermanual.wiki/Document/TemperatureHumidityDataLoggerCommandsAPI24.2837071165/html). The second element is the second packet. 

The `translate` function can then be used to decode the packets that have been detected. It currently only works for the first packet (as that's where most of the interesting data is) but could easily be expanded to decode the second as well. It returns the decoded packet in the form of a dictionary.

## Quickstart Example
```python
import BlueMaestroAPI as blm

raw_data = blm.scan(timeout = 20)
info = blm.translate(raw_data[0])

print(info[temperature], info[humidity], info[batt_lvl])
```
  
This example scans for Blue Maestro advertising packets for 20 seconds and prints the temperature, humidity and battery level.
