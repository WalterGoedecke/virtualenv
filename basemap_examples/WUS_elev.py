# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 16:21:39 2015

@author: walter
"""

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# read in etopo5 topography/bathymetry.
url = 'http://ferret.pmel.noaa.gov/thredds/dodsC/data/PMEL/etopo5.nc'
etopodata = Dataset(url)

topoin = etopodata.variables['ROSE'][:]
lons = etopodata.variables['ETOPO05_X'][:]
lats = etopodata.variables['ETOPO05_Y'][:]
# shift data so lons go from -180 to 180 instead of 20 to 380.
topoin,lons = shiftgrid(180.,topoin,lons,start=False)

# plot topography/bathymetry as an image.

# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.15, 0.15, 1.2, 1.2])

# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
#m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='l',area_thresh=1000.,projection='lcc',\
#            lat_1=50.,lon_0=-107.,ax=ax)
#m = Basemap(llcrnrlon=-119.8, llcrnrlat=32.3, urcrnrlon=-102.0, \
#            urcrnrlat=41.0, rsphere=(6378137.00,6356752.3142),\
#            resolution='l',area_thresh=1000.,projection='lcc',\
#            lat_1=50.,lon_0=-107.,ax=ax)
#m = Basemap(llcrnrlon=-118.5, llcrnrlat=35.0, urcrnrlon=-116.0, \
#            urcrnrlat=37.0, rsphere=(6378137.00,6356752.3142),\
#            resolution='l',area_thresh=1000.,projection='lcc',\
#            lat_1=35.5,lon_0=-117.,ax=ax)
# make orthographic basemap.
#m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
#m = Basemap(llcrnrlon=-118.5, llcrnrlat=35.0, urcrnrlon=-116.0, \
#            urcrnrlat=37.0, \
#            resolution='c', area_thresh=1000.,projection='cyl',\
#            lat_0=35.5, lon_0=-117., ax=ax)
m = Basemap(width=1000, height=1000, \
            resolution='c', area_thresh=1000.,projection='cyl',\
            lat_0=35.5, lon_0=-117., ax=ax)
#m = Basemap(resolution='c',projection='ortho',lat_0=35.5, lon_0=-117.0)

# nylat, nylon are lat/lon of New York
nylat = 40.78; nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53; lonlon = 0.08

# Draw great circle route between Los Angeles and Las Vegas
# LAlat, LAylon are lat/lon of Los Angeles
LAlat = 34.008; LAlon = -118.38
# LVlat, LVlon are lat/lon of Las Vegas.
LVlat = 36.03; LVlon = -114.36
# Draw the great circle 
m.drawgreatcircle(LAlon, LAlat, LVlon, LVlat, linewidth=1, \
    color='r')
    
#######################
# Plot chalk sites. 
# # # # # # # # # # # #
# L-20. 
L20lat = 35.699390
L20lon = -117.626023
x, y = m(L20lon, L20lat)
#m.plot(x, y, 'ko', markersize=3)
m.plot(x, y, 'k^', markersize=4)
#plt.text(x, y, 'L', fontsize=14, fontweight='bold', ha='center', va='center', color='b')
label = 'L-20'
#z = zip(labels, x, y)
#plt.text(x+10000, y+5000, label, fontsize=5)
plt.text(x+4000, y+3000, label, fontsize=6)
# # # # # # # # # # # #
# Rotr1. 
R1lat = 35.76873778
R1lon = -117.7756747
x, y = m(R1lon, R1lat)
m.plot(x, y, 'bo', markersize=3)
label = 'ROTR 1'
plt.text(x+4000, y+0, label, fontsize=6)
# # # # # # # # # # # #
# Rotr2. 
R2lat = 35.85866406
R2lon = -117.5768854
x, y = m(R2lon, R2lat)
m.plot(x, y, 'ro', markersize=3)
label = 'ROTR 2'
plt.text(x+4000, y+3000, label, fontsize=6)
# # # # # # # # # # # #
# Rotr3. 
R3lat = 35.77147283
R3lon = -117.7761122
x, y = m(R3lon, R3lat)
m.plot(x, y, 'go', markersize=3)
label = 'ROTR 3'
plt.text(x+4000, y+3000, label, fontsize=6)
# # # # # # # # # # # #
# Rotr4. 
R4lat = 35.89375766
R4lon = -117.6123566
x, y = m(R4lon, R4lat)
m.plot(x, y, 'yo', markersize=3)
label = 'ROTR 4'
plt.text(x+4000, y+3000, label, fontsize=6)
#######################

# transform to nx x ny regularly spaced 5km native projection grid
nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map with imshow.
im = m.imshow(topodat,cm.GMT_haxby)
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# draw parallels and meridians.
# label on left and bottom of map.
parallels = np.arange(0.,80,20.)
m.drawparallels(parallels,labels=[1,0,0,1])
meridians = np.arange(10.,360.,30.)
m.drawmeridians(meridians,labels=[1,0,0,1])
# add colorbar
cb = m.colorbar(im,"right", size="5%", pad='2%')
ax.set_title('ETOPO5 Topography - Lambert Conformal Conic')
plt.show()

# Save figure. 
fig.savefig("WUS_elev.png")
