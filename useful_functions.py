
import json
import pandas as pd
import xarray as xr
import yaml
import datetime
import time
from itertools import dropwhile
import sys 
import os
import subprocess
from eccodes import *
import requests
import argparse
from io import StringIO
import logging
from logging.handlers import TimedRotatingFileHandler
import matplotlib.pyplot as plt
import numpy as np
import traceback
from SPARQLWrapper import SPARQLWrapper, JSON
import operator
import re

## SOME USEFUL FUNCTIONS

def copy_dict(d, *keys):
    #Make a copy of only the `keys` from dictionary `d`
    liste = []
    for i in d:
        try:
            liste.append({key: i[key] for key in keys})
        except:
            continue
    return liste 


def floatorint(x):
    # checks if string should be float or int or just a string
    try:
        if '.' in x:
            return(float(x))
        else:
            return(int(x))
    except:
        return(x)


def filter_section(message):
    # filters the section for stuff
    # can work on this to take in arguments for filtering a specified type of variable 
    filtered = []
    for m in message:
        try:
            if m['value'] == None:
                continue
            if m['key'] == 'shortDelayedDescriptorReplicationFactor':
                continue
            if m['key'] == 'delayedDescriptorReplicationFactor':
                continue
            if m['key'] == 'instrumentationForWindMeasurement':
                continue
            if m['key'] == 'timeSignificance':
                continue
            else:
                filtered.append(m)
        except:
            continue
            
    return filtered

def return_dictionary(blob, key, value):
    # returns the dictionary where the key is equal to a specific value

    return (list(filter(lambda item: item['{}'.format(key)] == '{}'.format(value), blob))[0])


def cf_match(key):
    # check if variable has a standard name 
    # this enpoint is giving you the CF standard names
    sparql = SPARQLWrapper("http://vocab.nerc.ac.uk/sparql/sparql") 
    #print(cfname)
    prefixes = '''
        prefix skos:<http://www.w3.org/2004/02/skos/core#>
        prefix text:<http://jena.apache.org/text#>
        prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix owl:<http://www.w3.org/2002/07/owl#> 
        prefix dc:<http://purl.org/dc/terms/>'''

    query = '''select distinct ?cfconcept WHERE {
       ?cf rdf:type skos:Collection . 
       ?cf skos:prefLabel "Climate and Forecast Standard Names" .
       ?cf skos:member ?cfconcept .
       ?cfconcept owl:deprecated "false" .
       ?cfconcept skos:prefLabel "%s"@en.   
      }'''
    
    sparql.setQuery(prefixes + query % (key))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    suggestion = '''SELECT ?cflabel WHERE {
        ?cf rdf:type skos:Collection .
        ?cf skos:prefLabel "Climate and Forecast Standard Names" .
        ?cf skos:member ?cfconcept .
        ?cfconcept owl:deprecated "false" .
        ?cfconcept skos:prefLabel ?cflabel .
        filter contains(?cflabel,"%s"@en)
      }'''
    
    if (results["results"]["bindings"]):
        return(key)
    else:
        return('fail')

def units(dfs):
    # if a new measurement is added to the station in the desired timeframe, then this function will make sure the unit for
    # that measurement is saved

    # can try to use pd.combine_first to maybe operate quicker

    dfs_to_check = dfs
    original_df = dfs[0]
    for df in dfs_to_check[1:]:
        for key in df['key']:
            if key not in original_df.key.values.tolist():
                original_df['key'] = df['key']
                original_df['units'] = df['units']               
                original_df['code'] = df['code']
            else:
                continue
    return original_df


def height(dfs):
    # does the same as the units-function
    dfs_to_check = dfs
    original_df = dfs[0]
    for df in dfs_to_check[1:]:
        for key in df['key']:
            if key not in original_df.key.values.tolist():
                original_df['key'] = df['key']
                original_df['height_numb'] = df['height_numb']               
                original_df['height_type'] = df['height_type']
            else:
                continue
    return original_df

def times(dfs):
    # does the same as the height-function, but for time
    dfs_to_check = dfs
    original_df = dfs[0]
    for df in dfs_to_check[1:]:
        for key in df['key']:
            if key not in original_df.key.values.tolist():
                original_df['key'] = df['key']
                original_df['time_duration'] = df['time_duration']    
            else:
                continue           
    return original_df
                
                
def instrumentation_code_flag(value):
    dictionary = {'0': 'AUTOMATIC STATION', '1': 'MANNED STATION', '2': 'HYBRID, BOTH MANNED AND AUTOMATIC', '3': ''}
    return dictionary[value]
print(instrumentation_code_flag('0'))


#¤def flags_that_matter(flag, value):
#    dictionary = {'020003':
#                    ''}
#    return