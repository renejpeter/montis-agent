import os
from pySMART import Device

class SMART:
    def __init__(self):
        self.deviceList = list()

    # run smartctl in cli
    def RunSmartCtl(self, strArgs):
        cmdString = "smartctl " + strArgs
        output = os.popen(cmdString).read()
        return str.splitlines(output)

    # get all device ids
    def GetDeviceIds(self):
        lines = self.RunSmartCtl("--scan")
        for line in lines:
            deviceId = str.split(line, " " ,1)[0]
            self.deviceList.append(deviceId)

    # get device info
    def GetDeviceInfo(self, deviceId):
        item = {}
        deviceInfoLines = self.RunSmartCtl("-i " + deviceId)
        bEnteredInfoSection = False
        item['deviceId'] = deviceId
        for line2 in deviceInfoLines:
            if not bEnteredInfoSection:
                if line2.lower() == "=== start of information section ===":
                    bEnteredInfoSection = True
            else:
                field = str.split(line2, ":", 1)
                #get model family
                if field[0].lower() == "model family":
                    item['family'] = field[1].strip()
                #get device model
                elif field[0].lower() == "device model":
                    item['model'] = field[1].strip()
                #get serial number
                elif field[0].lower() == "serial number":
                    item['serial'] = field[1].strip()
                #get device firmware version
                elif field[0].lower() == "firmware version":
                    item['firmware'] = field[1].strip()
                #get device capacity
                elif field[0].lower() == "user capacity":
                    item['capacity'] = field[1].strip()
                #get sector sizes
                elif field[0].lower() == "sector sizes":
                    item['sectorSize'] = field[1].strip()
                #get rotation rate
                elif field[0].lower() == "rotation rate":
                    item['rotationRate'] = field[1].strip()
                #get ata version
                elif field[0].lower() == "ata version is":
                    item['versionATA'] = field[1].strip()
                #get sata version
                elif field[0].lower() == "sata version is":
                    item['versionSATA'] = field[1].strip()
                #get smart support status
                elif field[0].lower() == "smart support is":
                    temp = str.split(field[1].strip(), " ", 1)
                    strTemp = temp[0].strip().lower()

                    if strTemp == "available":
                        item['smartSupport'] = 'yes'
                    elif strTemp == "unavailable":
                        item['smartSupport'] = 'no'                      
                        item['smartSupportEnabled'] = 'no'
                    elif strTemp == "enabled":
                        item['smartSupportEnabled'] = 'yes'
                    elif strTemp == "disabled":
                        item['smartSupport'] = 'no'
        assess = Device(deviceId)
        item['smartStatus'] = assess.assessment
        return item

    # get all devices and their info
    def getInfo(self):
        self.GetDeviceIds()
        data = []
        for dvc in self.deviceList:
            data.append(self.GetDeviceInfo(dvc))
        return data