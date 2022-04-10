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

### GETTING TO KNOW THE FILES ####
file = open('output.json')
data = json.load(file)

number_of_stations = 0
stations_with_many_subsets = 0
jPzE952eWr2#r?y+H(
#new_array = np.array()
liste = [ [] for _ in range(5670) ]  #5670 er antall meldinger i bufr-filen, kan lett hentes ut ved hjelp av eccodes
count = 0
for message in data['messages'][:56]:
    if message['value'] == 1:
        count += 1
    liste[count-1].append(message)

blob = liste[0]
print(blob)
# shift from json to pandas dataframe



#print(stations_with_many_subsets)

#first_list = []
#for i in range(number_of_stations):
#    if message[i]['key'] == 'subsetNumber':
#        new_list = []
#    new_list.append(message[i])
    #first_list.append(new_list)        

#list(filter(lambda person: person['key'] == 'subsetNumber', data['messages']))

#print(first_list[i])
