import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import time

#function that scans for Blue Maestro's advertisment packets and returns them as a list
def scan(timeout: float = 30):

    #initialise list to store the two packets that the sensor broadcasts
    data_lst = [None, None]

    #callback function which is triggered everytime a new BLE device is found or changed
    def callback(device: BLEDevice, advertisement_data: AdvertisementData):

        #checks if the advertisement data contains Blue Maestro's unique manufacturer number
        data = advertisement_data.manufacturer_data.get(307)

        #if <data> is None than simply continue scanning
        if not data:
            return
        
        #if the length of the byte is 14 then it is the first byte and will be stored in <data_lst> in position 0
        elif len(data) == 14:
            data_lst[0] = data

        #if the length of the byte is 25 then it is the second byte and will be stored in <data_lst> in position 1
        elif len(data) == 25:
            data_lst[1] = data

    #function that scans for new/changed BLE devices and registers a callback
    async def run(timeout):
        scanner = BleakScanner()
        scanner.register_detection_callback(callback)

        #define how long to scan for based on <timeout> argument
        t_end = time.time() + timeout

        #while loop will run and continue scanning as long as either element of <data_lst> is empty and the time is less than the specified timeout
        while data_lst[0]==None and data_lst[1]==None and time.time() < t_end:
            await scanner.start()
            await asyncio.sleep(5.0)
            await scanner.stop()

    #runs both the functions we defined earlier
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(timeout))
    loop.stop()

    error_msg = 'No Blue Maestro packets detected'

    #returns <data_lst> if it managed to pick up either packet
    if data_lst[0]==None and data_lst[1]==None:
        raise RuntimeError(error_msg)
    else:
        return data_lst

#function takes the packet scanned by the <scan_for_data> function and decodes it
#this function only works for the first packet as that is where most of the useful information is
def translate(pckt: bytes):
    info = {}
    
    #decodes the packet based on the positioning given in Blue Maestro's Temperature Humidity Data Logger Commands API 2.4
    #can be found here: https://usermanual.wiki/Document/TemperatureHumidityDataLoggerCommandsAPI24.2837071165/html
    info["version"] = int.from_bytes(pckt[0:1], byteorder='big')
    info["batt_lvl"] = int.from_bytes(pckt[1:2], byteorder='big')
    info["interval"] = int.from_bytes(pckt[2:4], byteorder='big')
    info["log_count"] = int.from_bytes(pckt[4:6], byteorder='big')
    info["temperature"] = int.from_bytes(pckt[6:8], byteorder='big', signed=True) / 10
    info["humidity"] = int.from_bytes(pckt[8:10], byteorder='big', signed=True) / 10
    info["dew_point"] = int.from_bytes(pckt[10:12], byteorder='big', signed=True) / 10

    return info

#to test if functions are working as expected
if __name__ == '__main__':
    raw_data = scan(timeout=15)
    decoded_data = translate(raw_data[0])
    print(decoded_data)
