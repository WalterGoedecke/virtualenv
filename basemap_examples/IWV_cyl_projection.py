# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:03:34 2015

@author: walter
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

# create new figure, axes instances.
fig=plt.figure()
# Figure size. 
#ax=fig.add_axes([0.1,0.1,0.8,0.8])
#ax=fig.add_axes([0.15, 0.15, 1.2, 1.2])

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
#m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
#            llcrnrlon=-180,urcrnrlon=180,resolution='c')

#m = Basemap(llcrnrlon=-118.5, llcrnrlat=35.0, urcrnrlon=-116.0, \
#            urcrnrlat=37.0, \
#            resolution='c', area_thresh=1000.,projection='cyl',\
#            lat_0=35.5, lon_0=-117., ax=ax)

m = Basemap(projection='cyl', llcrnrlat=35.0, urcrnrlat=37.0,\
            llcrnrlon=-118.5, urcrnrlon=-116.0, resolution='l',\
            area_thresh=1000.)

#######################
# Plot chalk sites. 
# # # # # # # # # # # #
# L-20. 
L20lat = 35.699390
L20lon = -117.626023
x, y = m(L20lon, L20lat)
#m.plot(x, y, 'ko', markersize=3)
m.plot(x, y, 'k^', markersize=3)
#plt.text(x, y, 'L', fontsize=14, fontweight='bold', ha='center', va='center', color='b')
label = 'L-20'
#z = zip(labels, x, y)
#plt.text(x+10000, y+5000, label, fontsize=5)
plt.text(x+.02, y+.02, label, fontsize=5)
# # # # # # # # # # # #
# Rotr1. 
R1lat = 35.76873778
R1lon = -117.7756747
x, y = m(R1lon, R1lat)
m.plot(x, y, 'bo', markersize=2)
label = 'ROTR 1'
plt.text(x+.02, y+.02, label, fontsize=5)
# # # # # # # # # # # #
# Rotr2. 
R2lat = 35.85866406
R2lon = -117.5768854
x, y = m(R2lon, R2lat)
m.plot(x, y, 'ro', markersize=2)
label = 'ROTR 2'
plt.text(x+.02, y+.02, label, fontsize=5)
# # # # # # # # # # # #
# Rotr3. 
R3lat = 35.77147283
R3lon = -117.7761122
x, y = m(R3lon, R3lat)
m.plot(x, y, 'go', markersize=2)
label = 'ROTR 3'
plt.text(x+.02, y-.04, label, fontsize=5)
# # # # # # # # # # # #
# Rotr4. 
R4lat = 35.89375766
R4lon = -117.6123566
x, y = m(R4lon, R4lat)
m.plot(x, y, 'yo', markersize=2)
label = 'ROTR 4'
plt.text(x+.02, y+.02, label, fontsize=5)
# # # # # # # # # # # #
# B-mtn. 
lat = 35.666088
lon = -117.598263
x, y = m(lon, lat)
m.plot(x, y, 'y+', markersize=2)
label = 'B-Mtn'
plt.text(x+.02, y-.05, label, fontsize=5)
# # # # # # # # # # # #
# Telescope Pk. 
lat = 36.169827
lon = -117.089208
x, y = m(lon, lat)
m.plot(x, y, 'b+', markersize=2)
label = 'Telescope Pk'
plt.text(x+.02, y+.02, label, fontsize=5)
#######################

# create light source object.
#from matplotlib.colors import LightSource
#ls = LightSource(azdeg = 90, altdeg = 20)
# convert data to rgb array including shading from light source.
# (must specify color map)
#rgb = ls.shade(topodat, cm.GMT_haxby)
#im = m.imshow(rgb)

m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='coral', lake_color='aqua')

# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')
plt.title("Equidistant Cylindrical Projection")
plt.show()

# Save figure. 
fig.savefig("IWV_cyl_projection.png")


