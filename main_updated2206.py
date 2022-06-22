## Author: KATARINA ANDERSEN
## Last modified:


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
from dateutil.relativedelta import relativedelta
from get_keywords import get_keywords
from code_tables import *
from useful_functions import *


desired_path = '../file_samples'


def parse_arguments():

    # gathers the commands

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c","--cfg",dest="cfgfile",
            help="Configuration file", required=True)
    args = parser.parse_args()

    if args.cfgfile is None:
        parser.print_help()
        parser.exit()
    return args.cfgfile





def parse_cfg(cfgfile):

    #reads configuration file

    with open(cfgfile, 'r') as ymlfile:
        cfgstr = yaml.full_load(ymlfile)
    return cfgstr





def get_files(desired_path):

    # gets a list of the files that we wish to look at

    files = []
    for file in os.listdir(desired_path):
        if file.endswith('.bufr'):
          # Create the filepath of particular file
            file_path = ('{}/{}'.format(desired_path,file))
            files.append(file_path)
    return files

get_files = get_files(desired_path)






def bufr_2_json(file):

    #open bufr file, convert to json (using "-j s") and load it with json.loads

    json_file = json.loads(subprocess.check_output("bufr_dump -j f {}".format(file), shell=True))
    
    # sorting so that each subset is a list of dictionary
    count = 0
    sorted_messages = []
    for message in json_file['messages']:
        if message['key'] == 'subsetNumber':
            count += 1
            sorted_messages.append([])
        else:
            try:
                sorted_messages[count-1].append({'key': message['key'], 'value': message['value'],
                                   'code': message['code'], 'units': message['units']})
            except:
                print('this did not work')
    
    # sorting so that height of measurement equipment is a variable attribute instead of variable
    final_message = []        
    for msg in sorted_messages:
        height_measurements = ['007006', '007030', '007031', '007032', '007033'] # might have to add more codes here, check: https://confluence.ecmwf.int/display/ECC/WMO%3D30+element+table
        count_height = 0
        storing_height = []
        variables_with_height = []
        for i in msg:
        
            # if variable is a height of sensor etc, check if it is none. If not none, then add it as an attribute
            # for the consecutive variables until next height of sensor.
            if i['code'] in height_measurements and i['value'] != None:
                count_height += 1
                storing_height.append(i)
            if i['code'] in height_measurements and i['value'] == None:
                count_height += 1
                storing_height.append(None)

            if count_height == 0:
                variables_with_height.append(i)
            if count_height != 0 and i['code'] not in height_measurements:
                if storing_height[count_height-1] != None and i['key'] != 'timePeriod':
                    i['height'] = storing_height[count_height-1]
                variables_with_height.append(i)
                
        final_message.append(variables_with_height)
    
        
    finale= []
    for msg in final_message:
        time_code = ['004024', '004025']
        count_time = 0
        variables_with_time = []
        storing_time = []
        for i in msg:
            if i['code'] in time_code and i['value'] != None:
                count_time += 1
                storing_time.append(i)
            if i['code'] in time_code and i['value'] == None:
                count_time += 1
                storing_time.append(None)

            if count_time == 0:
                variables_with_time.append(i)
            if count_time != 0 and i['code'] not in time_code:
                if storing_time[count_time-1] != None:
                    i['time'] = storing_time[count_time-1]
                variables_with_time.append(i)
        finale.append(variables_with_time) 
    return finale





def sorting_hat(get_files):
    cfg = parse_cfg(parse_arguments())
    stations = cfg['station_info']['stations']
    stations_dict = {i : [] for i in stations}
    for one_file in get_files:
        simple_file = bufr_2_json(one_file)
        for station in simple_file:
            #print(str(station[0]['value']) + str(station[1]['value']) + str(station[2]['value']) + str(station[3]['value']))
            if cfg['station_info']['identifier_type'] == 'blockNumber + stationNumber':
                if str(station[0]['value']).zfill(2) + str(station[1]['value']).zfill(3) in stations:
                    #print(str(station[0]['value']).zfill(2))
                    #print('{}'.format(str(station[0]['value']) + str(station[0]['value'])))
                    stations_dict['{}'.format(str(station[0]['value']).zfill(2) + str(station[1]['value']).zfill(3))].append(station)
            elif cfg['station_info']['identifier_type'] == 'wigosIdentifierSeries + wigosIssuerOfIdentifier + wigosIssueNumber + wigosLocalIdentifierCharacter':
                if str(station[0]['value']) + '-' + str(station[1]['value']) + '-' + str(station[2]['value']) + '-' + str(station[3]['value']) in stations:
                    stations_dict['{}'.format(str(station[0]['value']) + '-' + str(station[1]['value']) + '-' + str(station[2]['value']) + '-' + str(station[3]['value']))].append(station)
            elif cfg['station_info']['identifier_type'] == 'stateIdentifier + nationalStationNumber':
                if str(station[0]['value']) + str(station[1]['value']) in stations:
                    stations_dict['{}'.format(str(station[0]['value']) + str(station[1]['value']))].append(station)
            elif cfg['station_info']['identifier_type'] == 'shipOrMobileLandStationIdentifier':
                if str(station[0]['value']) in stations:
                        stations_dict['{}'.format(str(station[0]['value']))].append(station)
    print('sorting hat completed')
    return stations_dict






def block_and_station(msg):
    
    # storing data 
    gathered_df = []
    gathered_df_units = []
    gathered_df_height = []
    gathered_df_time = []
    
    #the following section is still messy, could probably be cleaned better
    #currently saving the values, units, height measurement and time resolution to each df and matching it up later
    #this is mostly because I find it easy to compare dfs
    
    for i in msg:
        
        height_copy = copy_dict(i,'key','height')
        dict_copy = filter_section(copy_dict(i,'key','value','units','code'))
        time_copy = copy_dict(i,'key','time')
        
        df = pd.DataFrame(dict_copy)
        
        #save a table with units for later use
        units_df = df
        units_df = units_df.drop(columns=['value'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':units_df['key'], 'usecols':None})._maybe_dedup_names(units_df['key'])
        units_df['key'] = cols # will add a ".1",".2" etc for each double name
        
        #save a table with height of measurement for later use
        height_df = pd.DataFrame(height_copy)
        height_df['height_numb'] = [str(val.get('value')) + ' ' + str(val.get('units')) for val in height_df.height]
        height_df['height_type'] = [str(val.get('key')) for val in height_df.height]
        height_df = height_df.drop(columns=['height'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':height_df['key'], 'usecols':None})._maybe_dedup_names(height_df['key'])
        height_df['key'] = cols # will add a ".1",".2" etc for each double name
        height_df = height_df.reset_index()
        
        #save a table with time of measurement for later use
        time_df = pd.DataFrame(time_copy)
        time_df['time_duration'] = [str(abs(val.get('value'))) + ' ' + str(val.get('units')) for val in time_df.time]
        time_df = time_df.drop(columns=['time'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':time_df['key'], 'usecols':None})._maybe_dedup_names(time_df['key'])
        time_df['key'] = cols # will add a ".1",".2" etc for each double name
        time_df = time_df.reset_index()
        
        #saving main table containing value of variables
        df = df.transpose().reset_index()
        df.columns = df.iloc[0]
        df = df[1:-2]
        df['time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])#.dt.strftime('%Y-%m-%d %H:%M')
        df = df.set_index('time')
        #some columnnames repeat itself, creating problems when changing to xarray. Fix with:
        cols = pd.io.parsers.base_parser.ParserBase({'names':df.columns, 'usecols':None})._maybe_dedup_names(df.columns)
        df.columns = cols # will add a ".1",".2" etc for each double name
        df = df.drop(columns=['key', 'year', 'month', 'day', 'hour', 'minute'])

        gathered_df.append(df)
        gathered_df_units.append(units_df)
        gathered_df_height.append(height_df)
        gathered_df_time.append(time_df)
    
    #sys.exit()    
    units_df = units(gathered_df_units).reset_index()
    height_df = height(gathered_df_height).reset_index()
    time_df = times(gathered_df_time).reset_index()
    main_df = pd.concat(gathered_df)
    
    #converting over to numeric. This becomes 64 bits, but since I haven't figured
    #out another way that converts string to either float32 or int32, this is the solution thus far 
    for column in main_df.columns:
        try:
            main_df[column] = pd.to_numeric(main_df[column])
        except:
            main_df[column] = main_df[column]
    
    #over to dataset
    main_ds = main_df.to_xarray()
    
    # Stuff that needs to be saved for later
    stationOrSiteName = main_df['stationOrSiteName'].values[0] # save for later
    main_ds = main_ds.drop_vars('stationOrSiteName')
    stationType = instrumentation_code_flag(str(main_ds['stationType'].values[0]))
    
    # need to get the set of keywords
    to_get_keywords = []
    
    # VARIABLE ATTRIBUTES
    for variable in main_ds.keys():
        var = variable
        if variable[-2] == '.':
            var = variable[:-2]
        change_upper_case = re.sub('(?<!^)(?=[A-Z])', '_', var).lower()
        
        # checking for standardname
        standardname_check = cf_match(change_upper_case)
        if standardname_check != 'fail':
            main_ds[variable].attrs['standard_name'] = standardname_check
        
        # adding long name. if variable has a height attribute, add it in the long name. if variable has a time attribute, add it in the long name.
        if variable in height_df.key.values.tolist():
            main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' measured at ' + 
                                                    height_df.loc[height_df['key'] == variable, 'height_numb'].iloc[0])
        elif variable in time_df.key.values.tolist():
            main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' with time duration of ' + 
                                                    time_df.loc[time_df['key'] == variable, 'time_duration'].iloc[0])
        elif variable in height_df.key.values.tolist() and variable in time_df.key.values.tolist():
                        main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' measured at ' +
                                                                height_df.loc[height_df['key'] == variable, 'height_numb'].iloc[0] + 
                                                                ' with time duration of ' + 
                                                                time_df.loc[time_df['key'] == variable, 'time_duration'].iloc[0])
        else:
            main_ds[variable].attrs['long_name'] = re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower()

        # add _FillValue    
        try:
            main_ds[variable] = main_ds[variable].fillna(-9999)
            main_ds[variable].attrs['_FillValue'] = -9999
        except:
            print('did not manage to fill value for', variable)
        
        # adding units, if units is a CODE TABLE or FLAG TABLE, it will overrule the previous set attributes to set new ones
        main_ds[variable].attrs['units'] = units_df.loc[units_df['key'] == variable, 'units'].iloc[0]
        if main_ds[variable].attrs['units'] == 'deg':
            main_ds[variable].attrs['units'] = 'degrees'
        if main_ds[variable].attrs['units'] == 'Numeric':
            main_ds[variable].attrs['units'] = 1
        if main_ds[variable].attrs['units'] == 'CODE TABLE':
            main_ds[variable].attrs['long_name'] = main_ds[variable].attrs['long_name'] + ' according to WMO code table ' + units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            del main_ds[variable].attrs['units']
        elif main_ds[variable].attrs['units'] == 'FLAG TABLE':
            main_ds[variable].attrs['long_name'] = main_ds[variable].attrs['long_name'] + ' according to WMO flag table ' + units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            del main_ds[variable].attrs['units']

            ####### IF WE WANT TO MAKE VARIABLES WITH CODE/FLAG TABLES AS FLAG VALUES #########

            """if main_ds[variable].attrs['units'] == 'CODE TABLE' or main_ds[variable].attrs['units'] == 'FLAG TABLE':
            code = units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            get_info = table_info(units_df.loc[units_df['key'] == variable, 'code'].iloc[0])
            if get_info == None:
                print(units_df.loc[units_df['key'] == variable, 'code'].iloc[0] + ' must be added to the table_info function')
            else:
                del main_ds[variable].attrs['units']
                main_ds[variable].attrs['standard_name'] = 'status_flag'
                main_ds[variable].attrs['long_name'] = get_info['long_name'].lower()
                main_ds[variable].attrs['flag_values'] = main_ds[variable].values
                print("','".join([str(a) for a in main_ds[variable].attrs['flag_values']]))
                main_ds[variable].attrs['flag_meanings'] = eval("table_{}(['{}'])".format(code, "','".join([str(a) for a in main_ds[variable].attrs['flag_values']])))
                main_ds[variable].attrs['valid_range'] = [int(get_info['valid_range'].split(",")[0]),  int(get_info['valid_range'].split(",")[1])]
                main_ds[variable].attrs['_FillValue'] = int(get_info['_FillValue'])"""
            
            #####################################################################################
        # adding coverage_content_type
        thematicClassification = ['blockNumber', 'stationNumber', 'stationType']
        coordinate = ['latitude', 'longitude']
        if variable in thematicClassification:
            main_ds[variable].attrs['coverage_content_type'] = 'thematicClassification'
        elif variable in coordinate:
            main_ds[variable].attrs['coverage_content_type'] = 'coordinate'
        else:
            main_ds[variable].attrs['coverage_content_type'] = 'physicalMeasurement'
        to_get_keywords.append(change_upper_case)

        # must rename if variable name starts with a digit
        timeunits = ['hour', 'second', 'minute', 'year', 'month', 'day']
        if change_upper_case[0].isdigit() == True and change_upper_case.split('_')[1].lower() in timeunits:
            fixing_varname = re.sub( r"([A-Z])", r" \1", variable).split()
            fixing_varname = fixing_varname[2:] + fixing_varname[:2] + ['s']
            fixing_varname = ''.join(fixing_varname)
            fixing_varname = fixing_varname[0].lower() + fixing_varname[1:]
            main_ds[fixing_varname] = main_ds[variable]
            main_ds = main_ds.drop([variable])
        
        # must also rename the ones that end with ".1"
        if variable[-2] == '.':
            new_name = variable.replace('.', '')
            main_ds[new_name] = main_ds[variable]
            main_ds = main_ds.drop([variable])
            
    main_ds['time'].attrs['long_name'] = 'time'
    main_ds['time'].attrs['standard_name'] = 'time'
    main_ds['time'].attrs['coverage_content_type'] = 'referenceInformation'   
    
    
    for var in main_ds.keys():
        if main_ds[var].dtype == 'int64':
            main_ds[var] = main_ds[var].astype(np.int32) 
        if main_ds[var].dtype == 'float64':
            main_ds[var] = main_ds[var].astype(np.float32) 
        else:
            continue


    keywords, keywords_voc = get_keywords(to_get_keywords)
    cfg = parse_cfg(parse_arguments())
    
    ################# REQUIRED GLOBAL ATTRIBUTES ###################
    # this probably might have to be modified

    main_ds.attrs['featureType'] = 'timeSeries'
    if stationOrSiteName == ' ':
         main_ds.attrs['id'] = str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3)
         main_ds.attrs['title'] = (str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + 
                                   ', ' + stationType)
    else:
        main_ds.attrs['id'] = str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + ', ' + stationOrSiteName
        main_ds.attrs['title'] = (str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + ', ' + stationOrSiteName
                                  + ', ' + stationType)
        
    main_ds.attrs['naming_authority'] = 'met.no'
    main_ds.attrs['summary'] = cfg['output']['abstract']
    main_ds.attrs['source'] = 'Synoptic measurements from ' + main_ds.attrs['id']
    main_ds.attrs['history'] = time.strftime('%Y-%m-%d %H:%M:')+': Data converted from BUFR to NetCDF-CF'
    main_ds.attrs['date_created'] = time.strftime('%Y-%m-%d %H:%M:%S')

    main_ds.attrs['geospatial_lat_min'] = '{:.3f}'.format(main_ds['latitude'].values.min())
    main_ds.attrs['geospatial_lat_max'] = '{:.3f}'.format(main_ds['latitude'].values.max())
    main_ds.attrs['geospatial_lon_min'] = '{:.3f}'.format(main_ds['longitude'].values.min())
    main_ds.attrs['geospatial_lon_max'] = '{:.3f}'.format(main_ds['longitude'].values.max())
    main_ds.attrs['time_coverage_start'] = main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime).strftime('%Y-%m-%d %H:%M:%S') # note that the datetime is changed to microsecond precision from nanosecon precision
    main_ds.attrs['time_coverage_end'] = main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime).strftime('%Y-%m-%d %H:%M:%S')
    
    duration_years = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).years)
    duration_months = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).months)
    duration_days = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).days)
    duration_hours = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).hours)
    duration_minutes = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).minutes)
    duration_seconds = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).seconds)
    main_ds.attrs['time_coverage_duration'] = ('P' + duration_years + 'Y' + duration_months +
                                               'M' + duration_days + 'DT' + duration_hours + 
                                               'H' + duration_minutes + 'M' + duration_seconds + 'S')    
    
    main_ds.attrs['keywords'] = keywords
    main_ds.attrs['keywords_vocabulary'] = keywords_voc
    main_ds.attrs['standard_name_vocabulary'] = 'CF Standard Name V79'
    main_ds.attrs['Conventions'] = 'ACDD-1.3, CF-1.6'

    main_ds.attrs['creator_type'] = ''
    main_ds.attrs['institution'] = cfg['author']['PrincipalInvestigatorOrganisation']
    main_ds.attrs['creator_name'] = cfg['author']['PrincipalInvestigator']
    main_ds.attrs['creator_email'] = cfg['author']['PrincipalInvestigatorEmail']
    main_ds.attrs['creator_url'] = cfg['author']['PrincipalInvestigatorOrganisationURL']
    main_ds.attrs['publisher_name'] = cfg['author']['Publisher']
    main_ds.attrs['publisher_email'] = cfg['author']['PublisherEmail']
    main_ds.attrs['publisher_url'] = cfg['author']['PublisherURL']
    main_ds.attrs['project'] = cfg['author']['Project']
    main_ds.attrs['license'] = cfg['author']['License']
    main_ds.attrs['processing_level'] = 'None'
    main_ds.attrs['references'] = 'None'
    
    return main_ds







def wigosnumber(msg):
# storing data 
    gathered_df = []
    gathered_df_units = []
    gathered_df_height = []
    gathered_df_time = []
    
    #the following section is still messy, could probably be cleaned better
    #currently saving the values, units, height measurement and time resolution to each df and matching it up later
    #this is mostly because I find it easy to compare dfs
    
    for i in msg:
        
        height_copy = copy_dict(i,'key','height')
        dict_copy = filter_section(copy_dict(i,'key','value','units','code'))
        time_copy = copy_dict(i,'key','time')
        
        df = pd.DataFrame(dict_copy)
        
        #save a table with units for later use
        units_df = df
        units_df = units_df.drop(columns=['value'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':units_df['key'], 'usecols':None})._maybe_dedup_names(units_df['key'])
        units_df['key'] = cols # will add a ".1",".2" etc for each double name
        
        #save a table with height of measurement for later use
        height_df = pd.DataFrame(height_copy)
        height_df['height_numb'] = [str(val.get('value')) + ' ' + str(val.get('units')) for val in height_df.height]
        height_df['height_type'] = [str(val.get('key')) for val in height_df.height]
        height_df = height_df.drop(columns=['height'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':height_df['key'], 'usecols':None})._maybe_dedup_names(height_df['key'])
        height_df['key'] = cols # will add a ".1",".2" etc for each double name
        height_df = height_df.reset_index()
        
        #save a table with time of measurement for later use
        time_df = pd.DataFrame(time_copy)
        time_df['time_duration'] = [str(abs(val.get('value'))) + ' ' + str(val.get('units')) for val in time_df.time]
        time_df = time_df.drop(columns=['time'])
        cols = pd.io.parsers.base_parser.ParserBase({'names':time_df['key'], 'usecols':None})._maybe_dedup_names(time_df['key'])
        time_df['key'] = cols # will add a ".1",".2" etc for each double name
        time_df = time_df.reset_index()
        
        #saving main table containing value of variables
        df = df.transpose().reset_index()
        df.columns = df.iloc[0]
        df = df[1:-2]
        df['time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])#.dt.strftime('%Y-%m-%d %H:%M')
        df = df.set_index('time')
        #some columnnames repeat itself, creating problems when changing to xarray. Fix with:
        cols = pd.io.parsers.base_parser.ParserBase({'names':df.columns, 'usecols':None})._maybe_dedup_names(df.columns)
        df.columns = cols # will add a ".1",".2" etc for each double name
        df = df.drop(columns=['key', 'year', 'month', 'day', 'hour', 'minute'])

        gathered_df.append(df)
        gathered_df_units.append(units_df)
        gathered_df_height.append(height_df)
        gathered_df_time.append(time_df)
    
    #sys.exit()    
    units_df = units(gathered_df_units).reset_index()
    height_df = height(gathered_df_height).reset_index()
    time_df = times(gathered_df_time).reset_index()
    main_df = pd.concat(gathered_df)
    
    #converting over to numeric. This becomes 64 bits, but since I haven't figured
    #out another way that converts string to either float32 or int32, this is the solution thus far 
    for column in main_df.columns:
        try:
            main_df[column] = pd.to_numeric(main_df[column])
        except:
            main_df[column] = main_df[column]
    
    #over to dataset
    main_ds = main_df.to_xarray()
    
    # Stuff that needs to be saved for later
    stationOrSiteName = main_df['stationOrSiteName'].values[0] # save for later
    main_ds = main_ds.drop_vars('stationOrSiteName')
    stationType = instrumentation_code_flag(str(main_ds['stationType'].values[0]))
    
    # need to get the set of keywords
    to_get_keywords = []
    
    # VARIABLE ATTRIBUTES
    for variable in main_ds.keys():
        var = variable
        if variable[-2] == '.':
            var = variable[:-2]
        change_upper_case = re.sub('(?<!^)(?=[A-Z])', '_', var).lower()
        
        # checking for standardname
        standardname_check = cf_match(change_upper_case)
        if standardname_check != 'fail':
            main_ds[variable].attrs['standard_name'] = standardname_check
        
        # adding long name. if variable has a height attribute, add it in the long name. if variable has a time attribute, add it in the long name.
        if variable in height_df.key.values.tolist():
            main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' measured at ' + 
                                                    height_df.loc[height_df['key'] == variable, 'height_numb'].iloc[0])
        elif variable in time_df.key.values.tolist():
            main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' with time duration of ' + 
                                                    time_df.loc[time_df['key'] == variable, 'time_duration'].iloc[0])
        elif variable in height_df.key.values.tolist() and variable in time_df.key.values.tolist():
                        main_ds[variable].attrs['long_name'] = (re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower() + ' measured at ' +
                                                                height_df.loc[height_df['key'] == variable, 'height_numb'].iloc[0] + 
                                                                ' with time duration of ' + 
                                                                time_df.loc[time_df['key'] == variable, 'time_duration'].iloc[0])
        else:
            main_ds[variable].attrs['long_name'] = re.sub( '(?<!^)(?=[A-Z])', ' ', var).lower()

        # add _FillValue    
        try:
            main_ds[variable] = main_ds[variable].fillna(-9999)
            main_ds[variable].attrs['_FillValue'] = -9999
        except:
            print('did not manage to fill value for', variable)
        
        # adding units, if units is a CODE TABLE or FLAG TABLE, it will overrule the previous set attributes to set new ones
        main_ds[variable].attrs['units'] = units_df.loc[units_df['key'] == variable, 'units'].iloc[0]
        if main_ds[variable].attrs['units'] == 'deg':
            main_ds[variable].attrs['units'] = 'degrees'
        if main_ds[variable].attrs['units'] == 'Numeric':
            main_ds[variable].attrs['units'] = 1
        if main_ds[variable].attrs['units'] == 'CODE TABLE':
            main_ds[variable].attrs['long_name'] = main_ds[variable].attrs['long_name'] + ' according to WMO code table ' + units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            del main_ds[variable].attrs['units']
        if main_ds[variable].attrs['units'] == 'FLAG TABLE':
            main_ds[variable].attrs['long_name'] = main_ds[variable].attrs['long_name'] + ' according to WMO flag table ' + units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            del main_ds[variable].attrs['units']

            ####### IF WE WANT TO MAKE VARIABLES WITH CODE/FLAG TABLES AS FLAG VALUES #########

            """code = units_df.loc[units_df['key'] == variable, 'code'].iloc[0]
            get_info = table_info(units_df.loc[units_df['key'] == variable, 'code'].iloc[0])
            if get_info == None:
                print(units_df.loc[units_df['key'] == variable, 'code'].iloc[0] + ' must be added to the table_info function')
            else:
                del main_ds[variable].attrs['units']
                main_ds[variable].attrs['standard_name'] = 'status_flag'
                main_ds[variable].attrs['long_name'] = get_info['long_name'].lower()
                main_ds[variable].attrs['flag_values'] = main_ds[variable].values
                print("','".join([str(a) for a in main_ds[variable].attrs['flag_values']]))
                main_ds[variable].attrs['flag_meanings'] = eval("table_{}(['{}'])".format(code, "','".join([str(a) for a in main_ds[variable].attrs['flag_values']])))
                main_ds[variable].attrs['valid_range'] = [int(get_info['valid_range'].split(",")[0]),  int(get_info['valid_range'].split(",")[1])]
                main_ds[variable].attrs['_FillValue'] = int(get_info['_FillValue'])"""
            
            #####################################################################################

                thematicClassification = ['blockNumber', 'stationNumber', 'stationType']
        coordinate = ['latitude', 'longitude']
        if variable in thematicClassification:
            main_ds[variable].attrs['coverage_content_type'] = 'thematicClassification'
        elif variable in coordinate:
            main_ds[variable].attrs['coverage_content_type'] = 'coordinate'
        else:
            main_ds[variable].attrs['coverage_content_type'] = 'physicalMeasurement'
        to_get_keywords.append(change_upper_case)

        # must rename if variable name starts with a digit
        timeunits = ['hour', 'second', 'minute', 'year', 'month', 'day']
        if change_upper_case[0].isdigit() == True and change_upper_case.split('_')[1].lower() in timeunits:
            fixing_varname = re.sub( r"([A-Z])", r" \1", variable).split()
            fixing_varname = fixing_varname[2:] + fixing_varname[:2] + ['s']
            fixing_varname = ''.join(fixing_varname)
            fixing_varname = fixing_varname[0].lower() + fixing_varname[1:]
            main_ds[fixing_varname] = main_ds[variable]
            main_ds = main_ds.drop([variable])
        
        # must also rename the ones that end with ".1"
        if variable[-2] == '.':
            new_name = variable.replace('.', '')
            main_ds[new_name] = main_ds[variable]
            main_ds = main_ds.drop([variable])
            
    main_ds['time'].attrs['long_name'] = 'time'
    main_ds['time'].attrs['standard_name'] = 'time'
    main_ds['time'].attrs['coverage_content_type'] = 'referenceInformation'   
    
    
    for var in main_ds.keys():
        if main_ds[var].dtype == 'int64':
            main_ds[var] = main_ds[var].astype(np.int32) 
        if main_ds[var].dtype == 'float64':
            main_ds[var] = main_ds[var].astype(np.float32) 
        else:
            continue


    keywords, keywords_voc = get_keywords(to_get_keywords)
    cfg = parse_cfg(parse_arguments())
    
    ################# REQUIRED GLOBAL ATTRIBUTES ###################
    # this probably might have to be modified

    main_ds.attrs['featureType'] = 'timeSeries'
    if stationOrSiteName == ' ':
         main_ds.attrs['id'] = str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3)
         main_ds.attrs['title'] = (str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + 
                                   ', ' + stationType)
    else:
        main_ds.attrs['id'] = str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + ', ' + stationOrSiteName
        main_ds.attrs['title'] = (str(main_ds['blockNumber'].values[0]).zfill(2) + str(main_ds['stationNumber'].values[0]).zfill(3) + ', ' + stationOrSiteName
                                  + ', ' + stationType)
        
    main_ds.attrs['naming_authority'] = 'met.no'
    main_ds.attrs['summary'] = cfg['output']['abstract']
    main_ds.attrs['source'] = 'Synoptic measurements from ' + main_ds.attrs['id']
    main_ds.attrs['history'] = time.strftime('%Y-%m-%d %H:%M:')+': Data converted from BUFR to NetCDF-CF'
    main_ds.attrs['date_created'] = time.strftime('%Y-%m-%d %H:%M:%S')

    main_ds.attrs['geospatial_lat_min'] = '{:.3f}'.format(main_ds['latitude'].values.min())
    main_ds.attrs['geospatial_lat_max'] = '{:.3f}'.format(main_ds['latitude'].values.max())
    main_ds.attrs['geospatial_lon_min'] = '{:.3f}'.format(main_ds['longitude'].values.min())
    main_ds.attrs['geospatial_lon_max'] = '{:.3f}'.format(main_ds['longitude'].values.max())
    main_ds.attrs['time_coverage_start'] = main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime).strftime('%Y-%m-%d %H:%M:%S') # note that the datetime is changed to microsecond precision from nanosecon precision
    main_ds.attrs['time_coverage_end'] = main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime).strftime('%Y-%m-%d %H:%M:%S')
    
    duration_years = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).years)
    duration_months = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).months)
    duration_days = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).days)
    duration_hours = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).hours)
    duration_minutes = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).minutes)
    duration_seconds = str(relativedelta(main_ds['time'].values[-1].astype('datetime64[s]').astype(datetime.datetime), main_ds['time'].values[0].astype('datetime64[s]').astype(datetime.datetime)).seconds)
    main_ds.attrs['time_coverage_duration'] = ('P' + duration_years + 'Y' + duration_months +
                                               'M' + duration_days + 'DT' + duration_hours + 
                                               'H' + duration_minutes + 'M' + duration_seconds + 'S')    
    
    main_ds.attrs['keywords'] = keywords
    main_ds.attrs['keywords_vocabulary'] = keywords_voc
    main_ds.attrs['standard_name_vocabulary'] = 'CF Standard Name V79'
    main_ds.attrs['Conventions'] = 'ACDD-1.3, CF-1.6'

    main_ds.attrs['creator_type'] = ''
    main_ds.attrs['institution'] = cfg['author']['PrincipalInvestigatorOrganisation']
    main_ds.attrs['creator_name'] = cfg['author']['PrincipalInvestigator']
    main_ds.attrs['creator_email'] = cfg['author']['PrincipalInvestigatorEmail']
    main_ds.attrs['creator_url'] = cfg['author']['PrincipalInvestigatorOrganisationURL']
    main_ds.attrs['publisher_name'] = cfg['author']['Publisher']
    main_ds.attrs['publisher_email'] = cfg['author']['PublisherEmail']
    main_ds.attrs['publisher_url'] = cfg['author']['PublisherURL']
    main_ds.attrs['project'] = cfg['author']['Project']
    main_ds.attrs['license'] = cfg['author']['License']
    main_ds.attrs['processing_level'] = 'None'
    main_ds.attrs['references'] = 'None'
    
    return main_ds







def stateidentifier(msg):
    gathered_df = []
    for i in range(len(msg)-1):
        
        dict_copy = copy_dict(msg[i], 'key','value')
        filtered_copy = filter_section(dict_copy)
        
        df = pd.DataFrame(filtered_copy).transpose().reset_index()
        df.columns = df.iloc[0]
        df = df[1:]
        df['time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']]).dt.strftime('%Y-%m-%d %H:%M')
        df = df.set_index('time')
        
        #some columnnames repeat itself, creating problems when changing to xarray. Fix with:
        cols = pd.io.parsers.ParserBase({'names':df.columns, 'usecols':None})._maybe_dedup_names(df.columns)
        df.columns = cols # will add a ".1",".2" etc for each double name
        
        df = df.drop(columns=['key', 'year', 'month', 'day', 'hour', 'minute'])
        
        gathered_df.append(df)
    main_df = pd.concat(gathered_df)
    main_ds = main_df.to_xarray()
    
    # adding attributes
    # need to fix for the ones with "~.1"  by adding an if-statement?
    
    for i in msg:
        for j in i:
            if j['key'] in main_ds.keys():
                main_ds[j['key']].attrs['standard_name'] = j['key']
                main_ds[j['key']].attrs['units'] = j['units']

            #figure out the keywords
            #first_try[i['key']].attrs['keywords'] = 

                try:
                    main_ds[j['key']].attrs['height'] = str(j['height']['value']) + ' ' + str(j['height']['units'])
                except:
                    continue
    
    
    # adding global attributes

    ## REQUIRED ATTRIBUTES ##
    # main_ds.attrs['id'] = blockNumber + StationNumber?
    # main_ds.attrs['naming_authority'] =
    # main_ds.attrs['title'] =
    # main_ds.attrs['summary'] =
    # main_ds.attrs['keywords'] =
    # main_ds.attrs['keywords_vocabulary'] =
    # main_ds.attrs['geospatial_lat_min'] = 
    # main_ds.attrs['geospatial_lon_min'] = 
    # main_ds.attrs['geospatial_lat_max'] = 
    # main_ds.attrs['geospatial_lon_max'] = 
    main_ds.attrs['time_coverage_start'] = (str(return_dictionary(msg[0], 'code', '004001')['value']) + '-' 
                                + str(return_dictionary(msg[0], 'code', '004002')['value']) + '-'
                                + str(return_dictionary(msg[0], 'code', '004003')['value']) + ' '
                                + str(return_dictionary(msg[0], 'code', '004004')['value']) + ':'
                                + str(return_dictionary(msg[0], 'code', '004005')['value']))
    main_ds.attrs['time_coverage_end'] = (str(return_dictionary(msg[-1], 'code', '004001')['value']) + '-'
                                + str(return_dictionary(msg[-1], 'code', '004002')['value']) + '-'
                                + str(return_dictionary(msg[-1], 'code', '004003')['value']) + ' '
                                + str(return_dictionary(msg[-1], 'code', '004004')['value']) + ':'
                                + str(return_dictionary(msg[-1], 'code', '004005')['value']))
    main_ds.attrs['Conventions'] = 'ACDD-1.3, CF-1.8'
    #main_ds.attrs['history'] = 
    #main_ds.attrs['date_created'] =
    #main_ds.attrs['creator_type'] =
    #main_ds.attrs['creator_institution'] =
    #main_ds.attrs['creator_name'] =
    #main_ds.attrs['creator_email'] =
    #main_ds.attrs['project'] =
    #main_ds.attrs['license'] =
    #main_ds.attrs['date_created'] = 

    ## OPTIONAL ATTRIBUTES ##
    #main_ds.encoding['_FillValue'] = None
    return main_ds





def shipOrMobileLandStationIdentifier(msg):
    gathered_ds = []
    for i in range(len(msg)-1):
        
        dict_copy = copy_dict(msg[i], 'key','value')
        filtered_copy = filter_section(dict_copy)
        
        df = pd.DataFrame(filtered_copy).transpose().reset_index()
        df.columns = df.iloc[0]
        df = df[1:]
        df['time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']]).dt.strftime('%Y-%m-%d %H:%M')
        df = df.set_index(['time', 'longitude', 'latitude'])
        
        #some columnnames repeat itself, creating problems when changing to xarray. Fix with:
        cols = pd.io.parsers.ParserBase({'names':df.columns, 'usecols':None})._maybe_dedup_names(df.columns)
        df.columns = cols # will add a ".1",".2" etc for each double name
        
        df = df.drop(columns=['key', 'year', 'month', 'day', 'hour', 'minute'])
        ds = df.to_xarray()
        gathered_ds.append(ds)
    final_ds = xr.merge(gathered_ds)
    return final_ds







def call_function():
    blobbing = sorting_hat(get_files[:3])
    stationtype = parse_cfg(parse_arguments())['station_info']['identifier_type']
    
    #{u: {'_FillValue': -999.0}}
    if stationtype == 'blockNumber + stationNumber':
        for key,val in blobbing.items():
            bla = block_and_station(blobbing['{}'.format(key)])
            bla.to_netcdf('new_test.nc',encoding={'time': {'units': 'seconds since 1970-01-01 00:00:00+0',
                                                           'dtype': 'int32'}})
    elif stationtype == 'wigosIdentifierSeries + wigosIssuerOfIdentifier + wigosIssueNumber + wigosLocalIdentifierCharacter':
        for key,val in blobbing.items():
            boom = wigosnumber(blobbing['{}'.format(key)])
            boom.to_netcdf('wigos_test.nc', encoding = {'time': {'units': 'seconds since 1970-01-01 00:00:00+0',
                                                                 'dtype': 'int32'}})
    elif stationtype == 'stateIdentifier + nationalStationNumber':
        for key,val in blobbing.items():
            print(stateidentifier(sorting_hat(get_files[:5])['{}'.format(key)]))
    elif stationtype == 'shipOrMobileLandStationIdentifier':
        for key,val in blobbing.items():
            print(shipOrMobileLandStationIdentifier(sorting_hat(get_files[:5])['{}'.format(key)]))

call_function()

#print(parse_cfg(parse_arguments()))
