def get_keywords(chosen_categories):
    keywords_dict = {'air_pressure': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SURFACE PRESSURE',
                    'air_temperature': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > AIR TEMPERATURE',
                    'dewpoint_temperature': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > DEW POINT TEMPERATURE',
                    'wind_speed': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED',
                    'wind_speed_of_gust': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED',
                    'wind_direction': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION',
                    'wind_from_direction': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION',
                    'relative_humidity': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > RELATIVE HUMIDITY',
                    'dew_point_temperature': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > DEW POINT TEMPERATURE',
                    'radiation': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > DOWNWELLING LONGWAVE RADIATION',
                    'surface_downwelling_longwave_flux_in_air': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > UPPWELLING LONGWAVE RADIATION',
                    'surface_upwelling_longwave_flux_in_air': 'GCMDSK:EARTH SCIENCE> ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > UPPWELLING LONGWAVE RADIATION',
                    'surface_downwelling_shortwave_flux_in_air': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SHORTWAVE RADIATION > DOWNWELLING SHORTWAVE RADIATION',
                    'surface_upwelling_shortwave_flux_in_air': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SHORTWAVE RADIATION > DOWNWELLING SHORTWAVE RADIATION',
                    'surface_albedo': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ALBEDO',
                    'surface_downwelling_photosynthetic_radiative_flux_in_air': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > RADIATIVE FLUX',
                    'surface_net_downward_radiative_flux': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION',
                    'total_sunshine': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SUNSHINE',
                    'height_of_station_ground_above_mean_sea_level': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ALTITUDE > STATION HEIGHT',
                    'pressure_reduced_to_mean_sea_level': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SEA LEVEL PRESSURE',
                    'characteristic_of_pressure_tendency': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE TENDENCY',
                    'total_precipitation_or_total_water_equivalent': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > PRECIPITATION >PRECIPITATION AMOUNT',
                    '3_hour_pressure_change':  'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE TENDENCY',
                    'present_weather': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS',
                    'past_weather1': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS',
                    'past_weather2': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS',
                    'direction_of_motion_of_moving_observing_platform': 'GCMDSK:WATER-BASED PLATFORMS',
                    'moving_observing_platform_speed': 'GCMDSK:WATER-BASED PLATFORMS',
                    'non_coordinate_pressure': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE',
                    'method_of_wet_bulb_temperature_measurement': 'GCMDSK:INSTRUMENT',
                    'wet_bulb_temperature': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE',
                    'horizontal_visibility': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > VISIBILITY',
                    'total_precipitation_past_24_hours': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT > 24 HOUR PRECIPITATION AMOUNT',
                    'cloud_cover_total': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD AMOUNT',
                    'cloud_amount': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD AMOUNT',
                    'height_of_base_of_cloud': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD BASE HEIGHT',
                    'cloud_type': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD TYPES',
                    'ice_deposit_thickness': 'GCMDSK:EARTH SCIENCE > OCEANS > SEA ICE > ICE DEPTH/THICKNESS',
                    'rate_of_ice_accretion_estimated': 'GCMDSK:EARTH SCIENCE > OCEANS > SEA ICE > ICE GROWTH/MELT',
                    'cause_of_ice_accretion': 'GCMDSK:EARTH SCIENCE > OCEANS > SEA ICE',
                    'sea_ice_concentration': 'GCMDSK:EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE CONCENTRATION',
                    'amount_and_type_of_ice': 'GCMDSK:EARTH SCIENCE > CRYOSPHERE > SNOW/ICE',
                    'ice_situation': 'GCMDSK:EARTH SCIENCE > CRYOSPHERE > SNOW/ICE',
                    'ice_development': 'GCMDSK:EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE GROWTH/MELT',
                    'ice_edge_bearing': 'GCMDSK:EARTH SCIENCE > CRYOSPHERE > SNOW/ICE',
                    'method_of_water_temperature_and_or_or_salinity_measurement': 'GCMDSK:INSTRUMENTS > IN SITU/LABORATORY INSTRUMENTS',
                    'oceanographic_water_temperature': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > WATER TEMPERATURE',
                    'depth_below_water_surface': 'GCMDSK:EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH',
                    'waves_direction': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE DIRECTION',
                    'period_of_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD',
                    'height_of_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE HEIGHT',
                    'wind_waves_direction': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WIND WAVES',
                    'period_of_wind_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WIND WAVES',
                    'height_of_wind_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES > WIND WAVES',
                    'swell_waves_direction': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES',
                    'period_of_swell_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES',
                    'height_of_swell_waves': 'GCMDSK:EARTH SCIENCE > OCEANS > OCEAN WAVES',
                    'maximum_temperature_at_height_and_over_period_specified': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE',
                    'minimum_temperature_at_height_and_over_period_specified': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE',
                    'instrumentation_for_wind_measurement': 'GCMDSK:INSTRUMENTS > IN SITU/LABORATORY INSTRUMENTS > CURRENT/WIND METERS',
                    'maximum_wind_gust_direction': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS',
                    'maximum_wind_gust_speed': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS',
                    'maximum_wind_speed_10_minute_mean_wind': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND SPEEDS',
                    '24_hour_pressure_change': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE',
                    'total_snow_depth': 'GCMDSK:EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW DEPTH',
                    'pressure': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE',
                    'non_coordinate_geopotential_height': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ALTITUDE > GEOPOTENTIAL HEIGHT',
                    'global_solar_radiation_integrated_over_period_specified': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR RADIATION',
                    'diffuse_solar_radiation_integrated_over_period_specified': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR RADIATION',
                    'evaporation': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > EVAPORATION',
                    'state_of_ground': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLIMATE INDICATOR',
                    'true_direction_from_which_a_phenomenon_or_clouds_are_moving_or_in_which_they_are_observed': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLOUDS',
                    'state_of_sky_in_tropics': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > CLIMATE INDICATOR',
                    'main_present_weather_detecting_system': 'GCMDSK:INSTRUMENTS',
                    'supplementary_present_weather_sensor': 'GCMDSK:INSTRUMENTS',
                    'visibility_measurement_system': 'GCMDSK:INSTRUMENTS',
                    'soil_temperature': 'GCMDSK:EARTH SCIENCE > AGRICULTURE > SOILS > SOIL TEMPERATURE',
                    'precipitation_intensity_high_accuracy': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > PRECIPITATION',
                    'precipitation_type': 'GCMDSK: EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICATORS',
                    'extreme_counterclockwise_wind_direction_of_a_variable_wind': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND DIRECTION',
                    'extreme_clockwise_wind_direction_of_a_variable_wind': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND DIRECTION',
                    'other_weather_phenomena': 'GCMDSK:EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS',
                }
    keywords_voc_dict = {'GCMDSK': 'GCMDSK:GCMD Science Keywords:https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/sciencekeywords',
                         'GCMDPROV': 'GCMDPROV:GCMD Providers:https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/providers',
                         'GCMDLOC': 'GCMDLOC:GCMD Locations:https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/locations'}
    keywords_list = []
    keywords_voc_list = []
    
    #the variables im unsure of/cant find
    variables_with_no_keywords = ['block_number', 'station_number', 'station_type', 'latitude', 'longitude', 
                                  'time_significance','vertical_significance_surface_observations',
                                  'ground_minimum_temperature_past_12_hours', 'observation_sequence_number',
                                  'method_of_snow_depth_measurement', 'type_of_instrumentation_for_evaporation_measurement',
                                  'bearing_or_azimuth', 'depth_below_land_surface', 'method_of_state_of_ground_measurement',
                                  'first_order_statistics', 'method_of_precipitation_measurement','method_of_liquid_content_measurement_of_precipitation',
                                  'phenomena_occurence', 'obstruction', 'maximum_diameter_of_hailstones', 'diameter_of_deposit',
                                  'cloud_detection_system', 'sky_condition_algorithm_type','attribute_of_following_value']
    for i in chosen_categories:
        if keywords_dict.get(i) != None:
            keywords_list.append(keywords_dict.get(i))
            keywords = keywords_dict.get(i)
            keywords = keywords.split(':')
            keywords_voc_list.append(keywords_voc_dict.get(keywords[0]))
        elif i in variables_with_no_keywords:
            continue
        else:
            print('{} is not listed in the keywords dictionary, must be added'.format(i))
            continue
        
    keywords_list = list(set(keywords_list)) # removes dupes
    keywords_voc_list = list(set(keywords_voc_list)) # removes dupes
    
    print(keywords_voc_list)
    return (','.join(keywords_list)), (','.join(keywords_voc_list)) #returns as one string with lineshift

"""
# must add:

ground_temperature is not listed in the keywords dictionary, must be added
"""