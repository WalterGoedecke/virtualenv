from django.db import models
from django.contrib import admin

#Python imports
from django.template.defaultfilters import slugify
import datetime 

# Import python settings, and defintion from app.
from SolarFS2c.settings import MEDIA_ROOT
from classic import SfsLight

# Geocoders
import pygeocoder, geocoder
# Pandas et al.
import pandas, pvlib
from pvlib.location import Location 
# Matplotlib routinesl.
import matplotlib
matplotlib.use('Agg') # Must have here - not after from matplotlib.~ commands. 
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib import pyplot

# Create your models here.

class MyProfile(models.Model):
    user = models.OneToOneField("auth.User")
    #date_of_birth = models.DateField()
    bio = models.TextField()

class Calculation(models.Model):
    # Geocode variables. 
    address = models.TextField(max_length=120, blank=True, null=True, verbose_name='Address')
    address_slug = models.SlugField(max_length=120, blank=True, null=True)
    formatted_address = models.TextField(max_length=120, null=True, blank=True)
    coordinates = models.CharField(max_length=80, blank=True, null=True, verbose_name='latitude, longitude')
    #elevation = models.CharField(max_length=60, blank=True, null=True, verbose_name='Elevation (AMSL)', default="None'")
    elevation = models.FloatField(default=0.0, blank=True, null=True)
    # Panda variables. 
    #begin = models.CharField(max_length=30, default='2015, 7, 1, 11', blank=True, null=True)
    #begin = models.DateField(max_length=30, null=True)
    begin = models.CharField(max_length=30, blank=True, null=True)
    end = models.CharField(max_length=30, default='2015, 7, 1, 12', blank=True, null=True)
    frequency = models.CharField(max_length=20, default='3Min', blank=True, null=True)
    time_sequence = models.TextField(max_length=600, null=True, blank=True)
    # pvlib variables. 
    ephem_sequence = models.TextField(max_length=6000, null=True, blank=True)
    statistics = models.TextField(max_length=300, null=True, blank=True)
    irradiance_sequence = models.TextField(max_length=6000, null=True, blank=True)
    # Solar panel specs.  
    panel_azimuth = models.FloatField(max_length=20, default=180, blank=True, null=True, verbose_name='Panel azimuth (degrees from north)')
    panel_tilt = models.FloatField(max_length=20, default=30, blank=True, null=True, verbose_name='Panel tilt (degrees from vertical)')
    doc =  models.CharField(max_length=80, blank=True, null=True)
    pix1 =  models.CharField(max_length=80, blank=True, null=True)
    pix2 =  models.CharField(max_length=80, blank=True, null=True)

    # Creates a slug name. 
    prepopulated_fields = {
                           "address_slug": ("address",),
    }
    
    def __str__(self):
        return self.address
        #return '%s %s' % (self.question, self.answer)

    # Gets latitude & longitude from address. 
    def address2llh(self, address):
        geoAddress = pygeocoder.Geocoder.geocode(self.address)
        self.formatted_address = geoAddress.formatted_address
        self.coordinates = geoAddress.coordinates

        # Use geocoder to get elevation in meters AMSL. 
        elevation = self.address2elev(self.address)
        self.elevation = elevation
        # pyemphem requires a numeric elevation value. 
        return Location(*geoAddress.coordinates, altitude = elevation, name = self.address)
        
    # geocoder gets elevation from address. (g.location) returns lat, long 
    def address2elev(self, address):
        g = geocoder.elevation(address)
        elevation = g.elevation
        if elevation is None:    
            elevation = 0    
        return elevation
    
    def ephemeris(self, begin, end, frequency):
        location = self.address2llh(self.address)

        # Invoke panda routine.
        strBegin = begin.split(',')
        intBegin = [int(x) for x in strBegin]
        strEnd = end.split(',')
        intEnd = [int(x) for x in strEnd]

        # Avoids the "..." ellipsis that appear in data. 
        pandas.set_option('display.max_rows', 1000000)
    
        timeSequence = pandas.date_range(
            start=datetime.datetime(intBegin[0], intBegin[1], intBegin[2], intBegin[3]), 
            end=datetime.datetime(intEnd[0], intEnd[1], intEnd[2], intEnd[3]), freq = frequency)
        #self.time_sequence = timeSequence

        ##################
        # Solar ephemeris.
        # # # # # # # # # # # # # 
        ephemSequence = pvlib.solarposition.pyephem(
            timeSequence, location).drop(
                ['apparent_elevation', 'apparent_azimuth', 
                'apparent_zenith', 'elevation'], axis=1)
        self.ephem_sequence = ephemSequence
        # Create plot figure file. 
        ephemSequence.plot()
        pix1_name = 'ephem_' + self.address_slug + '.png' 
        plot_path = MEDIA_ROOT + 'plots/' + pix1_name
        pyplot.savefig(plot_path)
        ##################

        # Solar ephemeris. 
        eph_seq = str(ephemSequence)
        eph_seq_lines = eph_seq.split('\n')
        self.time_sequence = eph_seq_lines

        # Compute statistics. 
        self.statistics  = ephemSequence.describe()

        ##################
        # Solar specifications.
        # # # # # # # # # # # # # 
        location = self.address2llh(self.address)
        solarZenith = ephemSequence['zenith']
        solarAzi = ephemSequence['azimuth']
        irradianceSequence = pvlib.clearsky.ineichen(timeSequence, location)
        
        DNI = irradianceSequence['dni']
        DB = SfsLight.directBeam(self.panel_tilt, solarZenith, self.panel_azimuth-solarAzi, DNI)  

        irradianceSequence['DB'] = DB
        self.irradiance_sequence = irradianceSequence

        irradianceSequence.plot()
        pix2_name = 'irrad_' + self.address_slug + '.png' 
        plot_path = MEDIA_ROOT + 'plots/' + pix2_name
        pyplot.savefig(plot_path)
        ##################

        # Create plot figure file. 
        '''ephemSequence.plot()
        plot_path = MEDIA_ROOT + 'plots/ephemSequence.png'
        pyplot.savefig(plot_path)'''

        return

    # Write data to file, that can be downloaded. 
    def write_data(self):
        doc_name = 'SolarFS_' + self.address_slug + '.dat' 
        self.doc = doc_name
        pix1_name = 'ephem_' + self.address_slug + '.png' 
        self.pix1 = pix1_name
        pix2_name = 'irrad_' + self.address_slug + '.png' 
        self.pix2 = pix2_name
        data_path = MEDIA_ROOT + 'docs/' + doc_name
        f = open(data_path,"w")
        f.write('Formatted address: %s\n' % self.formatted_address)
        f.write('Coordinates (latitude, longitude): %s\n' % str(self.coordinates))
        f.write('Elevation: (meters AMSL) %s\t(feet): %f\n\n' % ( str(self.elevation), self.elevation/0.3048 ))
        #### Pandas time sequence ####
        f.write('Time sequence:\n')
        f.write('Start: %s\n' % self.begin)
        f.write('Stop: %s\n' % self.end)
        f.write('Frequency: %s\n\n' % self.frequency)
        #### #### ####
        f.write('Ephemeris:\n %s\n\n' % self.ephem_sequence)
        f.write('Statistics:\n %s\n\n' % self.statistics)
        f.write('Irradiance:\n %s\n\n' % self.irradiance_sequence)
        f.close()
        return
    
    def save(self, *args, **kwargs):
        # Create slugs of title, Country, and State_or_Provincea thumbnail name of avatar. 
        self.address_slug = slugify(self.address)
        # Invoke 'address2llh' function. . 
        self.formatted_address = self.address2llh(self.address)
        # Solar calculations.
        self.ephemeris(self.begin, self.end, self.frequency)
        # Write data to file. 
        self.write_data()
        # Save all. 
        super(Calculation, self).save()

class CalculationAdmin(admin.ModelAdmin):
    search_fields = ["address"]
    display_fields = ["address"]
    # Creates a slug name within ~/admin/. 
    prepopulated_fields = {
                           "address_slug": ("address",), 
}


