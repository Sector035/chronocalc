#!/usr/bin/env python3

import argparse
import ephem
from ephem import degree
import json
from prettytable import PrettyTable
import requests
import sys

from dateutil import rrule, tz
from datetime import datetime, timedelta
import arrow

from timezonefinder import TimezoneFinder

def get_timezone(lon, lat):
    tf = TimezoneFinder()
    local_timezone = tf.timezone_at(lng=float(lon), lat=float(lat))
    return(local_timezone)

def get_elevation(lon, lat):
    constructurl = 'https://api.open-elevation.com/api/v1/lookup?locations='+str(lat)+','+str(lon)
    response = requests.get(url=constructurl)
    elevation = response.json()
    return(elevation['results'][0]['elevation'])

def get_moon_position(year, lon, lat, elevation, searchalt, searchaz):
    location = ephem.Observer()
    location.lon = lon
    location.lat = lat
    location.elevation = elevation
    pos = ephem.Moon()

    utc_timezone = tz.gettz('UTC')
    local_timezone = tz.gettz(get_timezone(lon, lat))
    
    startmoment = datetime(year, 1, 1, 0, 00, 00)
    endmoment = datetime(year, 12, 31 ,23, 59, 00)

    tab = PrettyTable()
    tab.field_names = ['Date and time', 'Altitude', 'Azimuth', 'Illumination']
    tab.align['Altitude'] = 'l'
    tab.align['Azimuth'] = 'l'

    empty_table = True

    for timewindow in rrule.rrule(rrule.MINUTELY, interval=15, dtstart=startmoment, until=endmoment):
        location.date = timewindow
        pos.compute(location)
        if abs(pos.alt /degree - searchalt) < 2 and abs(pos.az /degree - searchaz) < 2:
            tab.add_row([arrow.get(timewindow).to('UTC').to(local_timezone), round(pos.alt/degree,2), round(pos.az/degree,2), str(round(pos.moon_phase*100,1))+'%'])
            empty_table = False
    
    if empty_table:
        print('No possible solution found. Please check the given parameters.')
    else:
        print('\nOn the following dates and times the moon is closest to the given parameters:\n')
        print(tab)
        #print(pos.moon_phase)
    
def calculate_sun(results, lon, lat, elevation, searchalt, searchaz, calc_start, calc_end, accuracy):
    location = ephem.Observer()
    location.lon = lon
    location.lat = lat
    location.elevation = elevation
    pos = ephem.Sun()

    utc_timezone = tz.gettz('UTC')
    local_timezone = tz.gettz(get_timezone(lon, lat))

    for timewindow in rrule.rrule(rrule.MINUTELY, interval=accuracy, dtstart=calc_start, until=calc_end):
        location.date = timewindow
        pos.compute(location)
        if abs(pos.alt/degree - searchalt) < 3 and abs(pos.az/degree - searchaz) < 3:
            closeby = (abs(pos.alt/degree - searchalt) * abs(pos.az/degree - searchaz))
            results.append((round(pos.alt/degree,2), round(pos.az/degree,2), timewindow, closeby))

    results.sort(key=lambda results:results[3])
    return results

def get_sun_position(year, lon, lat, elevation, searchalt, searchaz, accuracy):
    utc_timezone = tz.gettz('UTC')
    local_timezone = tz.gettz(get_timezone(lon, lat))

    date_solstice = ephem.next_solstice(datetime(year, 1, 1, 0, 00, 00))
    date_solstice = date_solstice.datetime()
    date_solstice = date_solstice.replace(minute=0, second=0, microsecond=0)

    date_start = datetime(year, 1, 1, 0, 00, 00)
    date_end = datetime(year, 12, 31, 23, 59, 00)

    results1 = []
    calculate_sun(results1, lon, lat, elevation, searchalt, searchaz, date_start, date_solstice, accuracy)

    results2 = []
    calculate_sun(results2, lon, lat, elevation, searchalt, searchaz, date_solstice, date_end, accuracy)

    if len(results1) < 2:
        sys.exit('No possible solution found. Please check the given parameters.')
    # Define a nice table
    tab = PrettyTable()
    tab.field_names = ['Date and time', 'Altitude', 'Azimuth']
    tab.add_rows(
        [
            [arrow.get(results1[0][2]).to('UTC').to(local_timezone), results1[0][0], results1[0][1]],
            [arrow.get(results2[0][2]).to('UTC').to(local_timezone), results2[0][0], results2[0][1]],
        ]
    )
    print('\nOn the following dates and times the sun is closest to the given parameters:\n')
    print(tab)
    
def main():
    parser = argparse.ArgumentParser(description='ChronoCalc - Determine dates & times of sun or moon positions within a year, given the location.')
    needed = parser.add_argument_group('Required arguments')
    needed.add_argument('-y', type=int, dest='year', help='The year that you want to calculate (ie: 2017)')
    needed.add_argument('-lat', type=str, dest='lat', help='Latitude of the observers location in decimals (ie: 7.2332)')
    needed.add_argument('-lon', type=str, dest='lon', help='Longitude of the observers location in decimals (ie: 49.8731)')
    needed.add_argument('-alt', type=float, dest='alt', help='Altitude from the observers perspective in degrees (ie: 25.8)')
    needed.add_argument('-az', type=float, dest='az', help='Azimuth from the observers perspective indegrees (ie: 220.5)')
    parser.add_argument('--moon', dest='moon', action='store_true', default=False, help='Run the script to for the moon, instead of the sun.')
    parser.add_argument('--accurate', dest='accuracy', action='store_const', const=2, default=15, help='Run the script in high accuracy mode (2 min interval). Useful when nothing is found, for instance when the latitude is near the equator, around -2 to 2 degrees.')
    args = parser.parse_args()
    
    elevation = get_elevation(args.lon, args.lat)

    if args.moon:
        get_moon_position(args.year, args.lon, args.lat, elevation, args.alt, args.az)
    else:
        get_sun_position(args.year, args.lon, args.lat, elevation, args.alt, args.az, args.accuracy)

if __name__=="__main__":
    main()