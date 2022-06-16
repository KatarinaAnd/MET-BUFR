def get_keywords(chosen_category):
    benedict = {'air_pressure': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SURFACE PRESSURE',
                'air_temperature': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > AIR TEMPERATURE',
                'wind_speed': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED',
                'wind_speed_of_gust': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED',
                'wind_direction': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION',
                'wind_from_direction': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION',
                'relative_humidity': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > RELATIVE HUMIDITY',
                'dew_point_temperature': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > DEW POINT TEMPERATURE',
                'radiation': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > DOWNWELLING LONGWAVE RADIATION',
                'surface_downwelling_longwave_flux_in_air': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > UPPWELLING LONGWAVE RADIATION',
                'surface_upwelling_longwave_flux_in_air': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION > UPPWELLING LONGWAVE RADIATION',
                'surface_downwelling_shortwave_flux_in_air': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SHORTWAVE RADIATION > DOWNWELLING SHORTWAVE RADIATION',
                'surface_upwelling_shortwave_flux_in_air': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SHORTWAVE RADIATION > DOWNWELLING SHORTWAVE RADIATION',
                'surface_albedo': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ALBEDO',
                'surface_downwelling_photosynthetic_radiative_flux_in_air': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > RADIATIVE FLUX',
                'surface_net_downward_radiative_flux': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION',
                'height_of_station_ground_above_mean_sea_level': 'EARTH SCIENCE > ATMOSPHERE > ALTITUDE > STATION HEIGHT',
                'pressure_reduced_to_mean_sea_level': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SEA LEVEL PRESSURE',
                'characteristic_of_pressure_tendency': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE TENDENCY',
                'dewpoint_temperature': 'EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > DEW POINT TEMPERATURE',
                }
    if chosen_category not in benedict:
        print('{} is not listed in the keywords dictionary, must be added'.format(chosen_category))
    else:
        return benedict.get(chosen_category)