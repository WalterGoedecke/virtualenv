from django.db import models

# Create your models here.
from django.contrib import admin
from django.contrib.auth.models import User

'''Geocoder, to determine GPS coordinates from address.''' 
import pygeocoder

class Place(models.Model):
    Place_ID = models.CharField(max_length=6, blank=True, null=True, verbose_name='Place ID - leave blank')
    Address = models.CharField(max_length=40, blank=True, verbose_name="Address Name")
    Latitude = models.CharField(max_length=16, blank=True, null=True, verbose_name='GPS Latitude - leave blank')
    Longitude = models.CharField(max_length=16, blank=True, null=True, verbose_name='GPS Longitude - leave blank')
    Compute_GPS = models.BooleanField(default=True, verbose_name='Allow geocoder to compute GPS coordinates from Address')

    def __str__(self):
        return str(self.Address)
    
    '''Generate unique ID from object's primary key.''' 
    def genID(self, Place_ID, pk):
        self.Place_ID = str(self.pk)
        return 
        
    '''Gets latitude & longitude from address.''' 
    def address2GPS(self, Address):
        '''Avoid error crash.'''
        try:
            geoAddress = pygeocoder.Geocoder.geocode(self.Address)
            GPS_coordinates = geoAddress.coordinates
            self.Latitude = GPS_coordinates[0]
            self.Longitude = GPS_coordinates[1]
        except: 
            pass
        return 
        
    def save(self, *args, **kwargs):
        '''Invoke 'genID' function.''' 
        self.genID(self.Place_ID, self.pk)
        '''Invoke 'address2GPS' function.''' 
        self.address2GPS(self.Address)
        '''Save all.''' 
        super(Place, self).save()

class Person(models.Model):
    Person_ID = models.CharField(max_length=6, blank=True, null=True, verbose_name='Person ID - leave blank')
    Name = models.CharField(max_length=40, blank=True, null=True, verbose_name="Person's Name")
    Places = models.ManyToManyField(Place, blank=True, verbose_name="Link to Places")

    def __str__(self):
        return str(self.Name)
    
    '''Generate unique ID from object's primary key.''' 
    def genID(self, Person_ID, pk):
        self.Person_ID = str(self.pk)
        return 
        
    def save(self, *args, **kwargs):
        '''Invoke 'genID' function.''' 
        self.genID(self.Person_ID, self.pk)
        '''Save all.''' 
        super(Person, self).save()
