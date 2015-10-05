# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:31:44 2015
Plot of great circle with matplotlib's basemap.
@author: walter
"""

import mpl_toolkits
from mpl_toolkits import basemap
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# create new figure, axes instances.
fig=plt.figure()
# Figure size. 
#ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax=fig.add_axes([0.15, 0.15, 1.2, 1.2])

# setup mercator map projection.
#m = Basemap(llcrnrlon=-100.,llcrnrlat=20.,urcrnrlon=20.,urcrnrlat=60.,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='l',projection='merc',\
#            lat_0=40.,lon_0=-20.,lat_ts=20.)
m = Basemap(llcrnrlon=-119.0,llcrnrlat=33.5,urcrnrlon=-114.0,urcrnrlat=36.5,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=5.,lon_0=-5.,lat_ts=1.)
# nylat, nylon are lat/lon of New York
nylat = 40.78; nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53; lonlon = 0.08

# LAlat, LAylon are lat/lon of Los Angeles
LAlat = 34.008; LAlon = -118.38
# LVlat, LVlon are lat/lon of Las Vegas.
LVlat = 36.03; LVlon = -114.36

# draw great circle route between NY and London
#m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
# draw great circle route between NY and London
m.drawgreatcircle(LAlon, LAlat, LVlon, LVlat, linewidth=1, \
    color='r')

m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents()
#m.drawcounties()

# draw parallels
#m.drawparallels(np.arange(10, 90, 20),labels=[1, 1, 0, 1])
m.drawparallels(np.arange(33, 37, 1),labels=[1, 1, 0, 1])
# draw meridians
m.drawmeridians(np.arange(-119, -114, 1),labels=[1, 1, 0, 1])
ax.set_title('Great Circle from Los Angeles to Las Vegas')
plt.show()
# Save figure. 
fig.savefig("great_circle-LA-LV.png")


