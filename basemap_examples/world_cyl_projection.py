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
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')
plt.title("Equidistant Cylindrical Projection")
plt.show()

# Save figure. 
fig.savefig("world_cyl_projection.png")
