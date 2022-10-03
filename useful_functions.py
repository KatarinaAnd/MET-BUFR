
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
import math
from dateutil.relativedelta import relativedelta
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
            if m['key'] == 'past_weather1' or m['key'] == 'past_weather2':
                continue
            if m['key'].endswith('AtHeightAndOverPeriodSpecified') == True:
                continue
            if m['key'] == 'attribute_of_following_value':
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
        try:
            for key in df['key']:
                if key not in original_df['key'].tolist():
                    unit = (df.loc[df['key'] == key]['units'].values[0])
                    code = (df.loc[df['key'] == key]['code'].values[0])
                    add_row = pd.DataFrame({'key':['{}'.format(key)], 'units':['{}'.format(unit)], 'code':['{}'.format(code)]})
                    original_df = pd.concat([original_df,add_row],ignore_index=True,axis=0)
                else:
                    continue
        except:
            continue
    return original_df


def height(dfs):
    # does the same as the units-function
    dfs_to_check = dfs
    original_df = dfs[0]
    
    for df in dfs_to_check[1:]:
        try:
            for key in df['key']:
                if key not in original_df.key.values.tolist():
                    height_numb = (df.loc[df['key'] == key]['height_numb'].values[0])
                    height_type = (df.loc[df['key'] == key]['height_type'].values[0])
                    add_row = pd.DataFrame({'key':['{}'.format(key)], 'height_numb':['{}'.format(height_numb)], 'height_type':['{}'.format(height_type)]})
                    original_df = pd.concat([original_df,add_row],ignore_index=True,axis=0)
                else:
                    continue
        except:
            continue
    return original_df

def times(dfs):
    # does the same as the height-function, but for time
    dfs_to_check = dfs
    original_df = dfs[0]
    for df in dfs_to_check[1:]:
        try:
            for key in df['key']:
                if key not in original_df.key.values.tolist():
                    time_duration = (df.loc[df['key'] == key]['time_duration'].values[0])
                    add_row = pd.DataFrame({'key':['{}'.format(key)], 'time_duration':['{}'.format(time_duration)]})
                    original_df = pd.concat([original_df,add_row],ignore_index=True,axis=0)
                else:
                    continue           
        except:
            continue
    return original_df
                
                
def instrumentation_code_flag(value):
    dictionary = {'0': 'AUTOMATIC STATION', '1': 'MANNED STATION', '2': 'HYBRID, BOTH MANNED AND AUTOMATIC', '3': ''}
    return dictionary[value]

def check_ds(ds, variable):
    if variable in list(ds.keys()):
        var = ds[variable].values[0] 
        new_ds = ds.drop_vars([variable])
    else:
        var = None
        new_ds = ds
    return new_ds, var

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def check_if_last_hour_of_month(check_date):
    delta = datetime.timedelta(hours=1)
    next_day = check_date + delta
    if check_date.month != next_day.month:
        return True
    return False