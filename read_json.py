# reading files
import json
import pandas as pd
import xarray as xr
# import yaml
from datetime import datetime

# for command line to use ECcodes
import sys
import os
import subprocess

# jPzE952eWr2#r?y+H(

# for user arguments
import requests
import argparse
from io import StringIO

# for logging
import logging
from logging.handlers import TimedRotatingFileHandler

# might be important for later
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------

# need to create a logger


"""def initialise_logger(outputfile = './log'):
    # Check that logfile exists
    logdir = os.path.dirname(outputfile)
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except:
            raise IOError
    # Set up logging
    mylog = logging.getLogger()
    mylog.setLevel(logging.INFO)
    #logging.basicConfig(level=logging.INFO, 
    #        format='%(asctime)s - %(levelname)s - %(message)s')
    myformat = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(myformat)
    mylog.addHandler(console_handler)
    file_handler = logging.handlers.TimedRotatingFileHandler(
            outputfile,
            when='w0',
            interval=1,
            backupCount=7)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(myformat)
    mylog.addHandler(file_handler)

    return(mylog)"""

        n 
file = open('output.json')
data = json.load(file)

number_of_stations = 0
stations_with_many_subsets = 0

liste = [ [] for _ in range(5670) ]  #5670 er antall meldinger i bufr-filen, kan lett hentes ut ved hjelp av eccodes
count = 0
for message in data['messages'][:56]:
    if message['value'] == 1:
        count += 1
    liste[count-1].append(message)

blob = liste[0]
blob = blob[1:]

def return_dictionary(blob, key, value):

    # returns the dictionary where the key is equal to a specific value

    return (list(filter(lambda item: item['{}'.format(key)] == '{}'.format(value), blob))[0])

def blob_read(what_blob):
    blob = what_blob

    # remove all dictionaries with null-values from list
    new_blob = []
    for i in range(len(blob)):
        if blob[i]['value'] != None:
            new_blob.append(blob[i])
       
    # gather dates
    year = return_dictionary(new_blob, 'code', '004001')['value']
    month = return_dictionary(new_blob, 'code', '004002')['value']
    day = return_dictionary(new_blob, 'code', '004003')['value']
    hour = return_dictionary(new_blob, 'code', '004004')['value']
    minute = return_dictionary(new_blob, 'code', '004005')['value']

    # remove date dictionaries from list for (maybe not necessary?)
    del new_blob[next((index for (index, d) in enumerate(new_blob) if d["code"] == "004001"), None)]
    del new_blob[next((index for (index, d) in enumerate(new_blob) if d["code"] == "004002"), None)]
    del new_blob[next((index for (index, d) in enumerate(new_blob) if d["code"] == "004003"), None)]
    del new_blob[next((index for (index, d) in enumerate(new_blob) if d["code"] == "004004"), None)]
    del new_blob[next((index for (index, d) in enumerate(new_blob) if d["code"] == "004005"), None)]

    # get station details
    for i in range(len(new_blob)):

        # add system warnings!!!

        if new_blob[i]["key"] == "blockNumber":


            blockNumber = return_dictionary(new_blob, 'key', 'blockNumber')['value']
            stationNumber = return_dictionary(new_blob, 'key', 'stationNumber')['value']
            stationOrSiteName = return_dictionary(new_blob, 'key', 'stationOrSiteName')['value']
            stationType = return_dictionary(new_blob, 'key', 'stationType')['value']
            
            #identifier = str(blockNumber) + " " + str(stationNumber) + " " + str(stationOrSiteName) + " " + str(stationType)
        

        if new_blob[i]['key'] == "stateIdentifier":


            stateIdentifier = return_dictionary(new_blob, 'key', 'stateIdentifier')['value']
            nationalStationNumber = return_dictionary(new_blob, 'key', 'nationalStationNumber')['value']
            longStationName = return_dictionary(new_blob, 'key', 'longStationName')['value']
            stationType = return_dictionary(new_blob, 'key', 'stationType')['value']

            #identifier = str(stateIdentifier) + " " + str(nationalStationNumber) + " " + str(longStationName) + " " + str(stationType)
        
        
        else:
            break
    


    #print(json.dumps(new_blob, indent=4, sort_keys=True))

    return(year)


print(blob_read(blob))