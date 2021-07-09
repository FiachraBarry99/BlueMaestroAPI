# BlueMaestroAPI
#### An unofficial Python API for interacting with Blue Maestro's sensors.  

I wrote this for a project I was working on and figured I would share it as there is no official Blue Maestro API for desktop. Currently, it is just a Python module but I can package it up and make it available on pypi if there's interest. To use this API just download the BlueMaestroAPI.py file and place it in the directory you are working in. You also need to make sure you have bleak, asyncio and time installed. Asyncio and time are standard Python libraries but bleak is not. These can all be installed using `pip install <package name>`. 

## How it Works
The API uses the [bleak](https://github.com/hbldh/bleak) library to scan for advertising data packets and checks if they're Blue Maestro packets using the manufacturing number. If Blue Maestro packets are detected it will return them as a list of packets in their raw little endian encoded structure. The first element in the list will be the first packet according to the Blue Maestro guide which can be found [here](https://usermanual.wiki/Document/TemperatureHumidityDataLoggerCommandsAPI24.2837071165/html). The second element is the second packet. 

The `translate` function can then be used to decode the packets that have been detected. It currently only works for the first packet (as that's where most of the interesting data is) but could easily be expanded to decode the second as well. It returns the decoded packet in the form of a dictionary.

## Quickstart Example
```python
import BlueMaestroAPI as blm

raw_data = blm.scan(timeout = 20)
info = blm.translate(raw_data[0])

print(info[temperature], info[humidity], info[batt_lvl])
```
  
This example scans for Blue Maestro advertising packets for 20 seconds and prints the temperature, humidity and battery level. 

## Issues/Notes
I have tested this API pretty rigoursly on Windows but I had some issues trying to implement it in Linux. I think this is because the Linux backend (BlueZ) has a different way of handling the scan response payload but I am not entirely sure. I have not yet attempted to use this on Mac and would really appreciate if someone could test it out as I do not personally own one.

Please note this is the first ever API of this kind I have written, so any issues or suggestions you have please let me know. Even if you need a hand implementing the code in your project please don't hesitate to reach out.
