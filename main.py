from PyP100 import PyP110
from bluepy.btle import Scanner, DefaultDelegate
from ela.bluetooth.advertising.TagFactory import Tagfactory
from dotenv import load_dotenv
from ahuora.flowsheet import Flowsheet
import os

load_dotenv()

sensor_locations = {
    "P RHT 904C92": {
        "label": "Air-Dryer_out-Evap-in",
        "unitop": "air_dryer",
        "propkey": None,
    },
    "P RHT 904C90": {
        "label": "Air-Cond_out-Dryer_in",
        "unitop": "cond_air_out",
        "propkey": None,
    },
    "P TPROBE 0021F9": { 
        "label": "Air-Evap_out-Cond_in",
        "unitop": "evap_air_out",
        "propkey": None,
    },
    "P TPROBE 0021F8": {
        "label": "Prop-Compressor_out-Cond_in",
        "unitop": "compr_prop_out",
        "propkey": None,
    },
    "P TPROBE 0021F7": {
        "label": "Prop-Evap_out-Compressor_in",
        "unitop": "evap_prop_out",
        "propkey": None,
    },
    "Energy": {
        "label": "Total Power",
        "unitop": "compressor",
        "propkey": None,
    },
}

# ----------------- Flowsheet Setup --------------------

api = Flowsheet()

for key, value in sensor_locations.items():
    sensor_locations[key].id = api.get_property_id(value["unitop"],value["propkey"])


# ---------------- BLUETOOTH SETUP --------------------

## 
# @class ScanDelegate
# @brief scan delegate to catch and interpret bluetooth advertising events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
            # this gets called a lot every scan, not sure if that's bad
            #print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

## associate the delegate to the scanner and start it for 10.0 seconds
scanner = Scanner().withDelegate(ScanDelegate())

# ------------- Tapo Power Plug Setup ----------------------

p110 = PyP110.P110(os.getenv("TAPO_IP"), os.getenv("TAPO_ACCOUNT"), os.getenv("TAPO_PASSWORD")) 

p110.handshake() #Creates the cookies required for further methods
p110.login() #Sends credentials to the plug and creates AES Key and IV for further methods

#The P110 has all the same basic functions as the plugs and additionally allow for energy monitoring.
# print(p110.getEnergyUsage()) #Returns dict with all of the energy usage of the connected plu
#{'today_runtime': 27, 'month_runtime': 27, 'today_energy': 2, 'month_energy': 2, 'local_time': '2024-05-15 12:28:35', 'electricity_charge': [0, 0, 0], 'current_power': 1601933}
# -------------- MAIN LOOP ------------------------------
while True:
    print("Scanning")
    devices = scanner.scan(60.0)

    # ----------------- DATA PROCESSING ------------------

    ## display result get from scanner
    for dev in devices:
        if( isinstance(dev.rawData, bytes)):
            tag = Tagfactory.getInstance().getTag(dev.rawData)
            
            # skip devices that aren't ELA tags
            if(tag.formattedDataSensor == "VOID"):
                continue;
            
            # Find the tag name
            name = "UNNAMED"
            for (adtype, desc, value) in dev.getScanData():
                if(desc == "Complete Local Name"):
                    name = value
            
            #print("Device %s (%s), RSSI=%d dB, Interpreted ELA Data=%s, RawData=%s" % (dev.addr, dev.addrType, dev.rssi, Tagfactory.getInstance().getTag(dev.rawData).formattedDataSensor ,binascii.b2a_hex(dev.rawData).decode('ascii')))
            
            # write the data to the db
            for measurement, value in tag.fields().items():
                print("%s: writing %s:%s" % (name,measurement,value))
                if(name not in sensor_locations):
                    print(name + " not registered as a location, skipping")
                    continue
                location = sensor_locations[name]
                api.update_property(location.id, value)
    
    # Print the info from the tapo plug
    energy = p110.getEnergyUsage()
    location = sensor_locations["Energy"]
    api.update_property(location.id, energy["current_power"])
