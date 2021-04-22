#!/usr/bin/env python

import json
from montis import MONTIS

def toScreen(data):
    print(json.dumps(data, sort_keys=False, indent=4))

def toJson(data):
    return json.dumps(data)

def sendPing():
    print('sent!')

montis = MONTIS()
data = montis.collectInfo()
toScreen(data)