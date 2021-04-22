#!/usr/bin/env python

import os
import socket
import platform
import uptime
import time
import cpuinfo
import psutil
import numpy
import json
from smart import SMART

class MONTIS:
    def __init__(self):
        self.data = {}
        self.payload = ''

    # get hostname
    def getHostname(self):
        self.data['hostname'] = platform.node()

    # get local ip
    def getLocalIp(self):
        self.data['localIp'] = socket.gethostbyname(self.data['hostname'])

    # get OS information
    def getOsInfo(self):
        uname = platform.uname()
        self.data['platform'] = uname.system
        self.data['osRelease'] = uname.release
        self.data['osVersion'] = uname.version
        self.data['osArch'] = list(platform.architecture())[0]

    # get uptime
    def getUptime(self):
        time = float(uptime.uptime())
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        self.data['uptime'] = f"%d:%d:%d:%d" % (day, hour, minutes, seconds)

    # get last boot time
    def getLastBoot(self):
        self.data['lastBootTime'] = str(uptime.boottime())

    # get timezone offset
    def getTimezone(self):
        minute = (time.localtime().tm_gmtoff / 60) % 60
        hour = ((time.localtime().tm_gmtoff / 60) - minute) / 60
        utcOffset = "%.2d%.2d" %(hour, minute)
        if utcOffset[0] != '-':
            utcOffset = '+' + utcOffset
        self.data['tz'] = utcOffset

    # get cpu information
    def getCpuInfo(self):
        self.data['cpuLoad'] = list(psutil.getloadavg())
        self.data['cpuMeta'] = {}
        self.data['cpuMeta']['model'] = cpuinfo.get_cpu_info()['brand_raw']
        self.data['cpuMeta']['cores'] = psutil.cpu_count(False)
        self.data['cpuMeta']['threads'] = psutil.cpu_count(True)

    # get memory information
    def getMemoryInfo(self):
        memRaw = dict(psutil.virtual_memory()._asdict())
        self.data['memoryTotal'] = memRaw['total']
        self.data['memoryAvailable'] = memRaw['available']

    # get storage volumes
    def getVolumeInfo(self):
        vols = []
        volData = psutil.disk_partitions(False)
        for v in volData:
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
            vols.append(vol)
        self.data['volumes'] = vols

    # get physical disk smart information
    def getDiskInfo(self):
        smart = SMART()
        self.data['disks'] = smart.getInfo()

    # get nic info
    def getNetworkInfo(self):
        print('get network info')

    def collectInfo(self):
        self.getHostname()
        self.getLocalIp()
        self.getOsInfo()
        #self.getUptime()
        self.getLastBoot()
        self.getTimezone()
        self.getCpuInfo()
        self.getMemoryInfo()
        self.getVolumeInfo()
        self.getDiskInfo()
        self.getNetworkInfo()
        return self.data