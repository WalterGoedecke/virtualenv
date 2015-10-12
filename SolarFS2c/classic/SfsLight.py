import os
import unittest
import math
import numpy
import pandas
import pvlib

# tilt = 90 - elevation (altitude)
# azimuth
# North 0, East 90, South 180, West 270

deg2rad = math.pi / 180.0

def directNormalIrradianceClearSky(SZA, ETI):
    """
    SZA - Solar Zenith Angle in radians
    ETI - Extra Terrestrial Irradiance
    """
    pass

#def directBeam(tilt, SZA, azi, DNI):
def directBeam(degTilt, degSZA, degAzi, DNI):
    """
    tilt - panel tilt in radians
    SZA - Solar Zenith Angle in radians
    azi - relative azimuth between panel and sun
    DNI - Direct Normal Irradiance
    return - plane of array beam irradiance
    """
    tilt = degTilt*math.pi/180
    SZA = degSZA*math.pi/180
    azi = degAzi*math.pi/180
    
    # cos angle of incidence
    cosInc = numpy.cos(tilt) * numpy.cos(SZA) \
           + numpy.sin(tilt) * numpy.sin(SZA) \
           * numpy.cos(azi)
           
    print(cosInc)       
    print(DNI)       
    
    beam = DNI * cosInc
    beam[beam < 0.0] = 0.0
    print(beam)
    
    return beam

def diffuseSkyIsotropic(tilt, DHI):
    """
    tilt - panel tilt in radians
    DHI - Diffuse Horizontal Irradiance
    return - plane of array sky irradiance
    """

    return DHI * 0.5 * (1.0 + numpy.cos(tilt))

def diffuseSky(tilt, SZA, DHI, GHI):
    """
    tilt - panel tilt in radians
    SZA - Solar Zenith Angle in radians
    DHI - Diffuse Horizontal Irradiance
    GHI - Global Horizontal Irradiance
    return - plane of array sky irradiance
    """

    return DHI * 0.5 * (1.0 + numpy.cos(tilt)) \
         + GHI * 0.5 * (1.0 - numpy.cos(tilt)) \
               * (0.12 * SZA - 0.04)
