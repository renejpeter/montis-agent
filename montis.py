#!/usr/bin/env python

import os
import platform
import uptime
import time
import cpuinfo
import psutil
import numpy
import json
from smart import SMART

data = {}

# Hostname
data['hostname'] = platform.node()

# OS
uname = platform.uname()
data['platform'] = uname.system
data['osRelease'] = uname.release
data['osVersion'] = uname.version
data['osArch'] = list(platform.architecture())[0]

# Uptime
upttime = float(uptime.uptime())
uptday = upttime // (24 * 3600)
upttime = upttime % (24 * 3600)
upthour = upttime // 3600
upttime %= 3600
uptminutes = upttime // 60
upttime %= 60
uptseconds = upttime
data['uptime'] = f"%d:%d:%d:%d" % (uptday, upthour, uptminutes, uptseconds)

# Last Boot Time
data['lastBootTime'] = str(uptime.boottime())

# Timezone
def utcOffset():
    minute = (time.localtime().tm_gmtoff / 60) % 60
    hour = ((time.localtime().tm_gmtoff / 60) - minute) / 60
    utcoffset = "%.2d%.2d" %(hour, minute)
    if utcoffset[0] != '-':
        utcoffset = '+' + utcoffset
    return utcoffset
data['timezoneOffset'] = utcOffset()

# CPU
data['cpuMeta'] = {}
data['cpuMeta']['model'] = cpuinfo.get_cpu_info()['brand_raw']
data['cpuMeta']['cores'] = psutil.cpu_count(False)
data['cpuMeta']['threads'] = psutil.cpu_count(True)
data['cpuLoad'] = list(psutil.getloadavg())

# Memory
memRaw = dict(psutil.virtual_memory()._asdict())
data['memoryTotal'] = memRaw['total']
data['memoryAvailable'] = memRaw['available']

# Storage Volumes
volumeData = psutil.disk_partitions(False)
data['volumes'] = []
for v in volumeData:
    if os.name == 'nt':
        if 'cdrom' in v.opts or v.fstype == '':
            continue
    usage = psutil.disk_usage(v.mountpoint)
    vol = {}
    vol['device'] = v.device
    vol['size'] = usage.total
    vol['used'] = usage.used
    vol['free'] = usage.free
    vol['formatType'] = v.fstype
    vol['mounted'] = v.mountpoint
    data['volumes'].append(vol)

# Physical Disks
smart = SMART()
data['disks'] = smart.getInfo()

# Save to JSON string
string = json.dumps(data, sort_keys=False, indent=4)

print(string)