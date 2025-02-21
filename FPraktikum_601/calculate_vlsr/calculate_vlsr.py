#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Required imports
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation
import astropy.units as u
from astropy.coordinates import Galactic, LSR


def vlsr(cfg,time='12:00:00-01-01-2025',l=90.,b=0.):
    '''Calculate the LSR_V velocity for a given time and location'''
    observatory_location = EarthLocation(lon=cfg.observatory_longitude*u.deg,\
        lat=cfg.observatory_latitude*u.deg, height=cfg.observatory_height*u.m)
    sky_coordinates = SkyCoord(l=l*u.deg, \
        b=b*u.deg,frame='galactic')
    split_time_dictionary = split_time(time)
    dtime = datetime(split_time_dictionary['year'],split_time_dictionary['month'],\
        split_time_dictionary['day'],hour=split_time_dictionary['hour'],\
        minute=split_time_dictionary['minute'],second=split_time_dictionary['second'])
    
    astro_time = Time(dtime, scale='utc')
    barycentric_v = sky_coordinates.radial_velocity_correction(kind='barycentric',\
        obstime=astro_time, location=observatory_location)  
    to_Galactic = Galactic(l=l*u.deg, \
        b=b*u.deg, pm_l_cosb=0*u.mas/u.yr, pm_b=0*u.mas/u.yr, \
        radial_velocity=barycentric_v, distance = 1.*u.pc)
    vlsr = to_Galactic.transform_to(LSR(v_bary=(10.27,15.32,7.74)*u.km/u.s)).radial_velocity
    return vlsr

def split_time(string_time):
    '''Split the time string into its components'''
    time_dictionary = {}
    time,day,month,year = string_time.split('-')
    hrs,min,sec=time.split(':')
    time_dictionary['hour'] = int(hrs)
    time_dictionary['minute'] = int(min)
    time_dictionary['second'] = int(sec)
    time_dictionary['day'] = int(day)
    time_dictionary['month'] = int(month)
    time_dictionary['year'] = int(year)
    return time_dictionary
