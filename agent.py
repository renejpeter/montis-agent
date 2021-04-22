#!/usr/bin/env python

import sys
import getopt
import json
from montis import MONTIS

outputFile = ''
outputFormat = 'json'

def toScreen(data):
    print(json.dumps(data, sort_keys=False, indent=4))

def toFile(data):
    print('saved to file!')

def toJson(data):
    return json.dumps(data)

def sendPing():
    print('sent!')

def main(argv):
    montis = MONTIS()
    data = montis.collectInfo()
    printToScreen = True
    outputFormat = 'json'
    outputFile = ''

    if printToScreen:
        toScreen(data)
    # if len(argv) > 0:
    #     opts, args = getopt.getopt(argv,"ho:f:p:",["output=","format=","ping="])

    #     for opt, arg in opts:
    #         if opt == '-h':
    #             print('agent.py -h -p -f <format> -o <outputfile>')
    #             sys.exit()

    #         if opt in ("-f", "--format"):
    #             if arg not in ("json", "xml"):
    #                 print('Invalid format, only JSON and XML are currently supported.')
    #                 sys.exit()
    #             outputFormat = arg
    #             print('format changed to: ' + outputFormat)

    #         if opt in ("-p", "--ping"):
    #             target = arg
    #             print('send post request with payload to target via https')
    #             # send post request with payload to target via https

    #         if opt in ("-o", "--output"):
    #             outputFile = arg
    #             # save to file
    #             print('saved to file: ' + outputFile)
    #             sys.exit()
    # else:
    #     toScreen(data)

if __name__ == "__main__":
   main(sys.argv[0:])