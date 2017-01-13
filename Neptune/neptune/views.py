from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.exceptions import *

from django.contrib.auth.decorators import login_required

from neptune.models import Person, Place
from neptune.forms import PersonForm, PlaceForm

'''Imports pagination.'''
from django.core.paginator import Paginator, InvalidPage, EmptyPage

'''JSON capability.'''
from django.http.response import HttpResponse
import json
from django.forms.models import model_to_dict
from django.core import serializers

''' Views listing of persons. ''' 
def person_list(request):

    persons = Person.objects.all()
    #If null, make the ID field the object's pk.
    for person in persons:
        if person.Person_ID == 'None':
            person.Person_ID = person.pk
            person.save()

    
    return render(request, "neptune/pages/person_list.html", add_csrf(request, persons=persons,
                                                                        ))
''' Views listing of places. ''' 
def place_list(request):

    places = Place.objects.all()
    #If null, this forces the ID field to assume the primary key value.
    for place in places:
        if place.Place_ID == 'None':
            place.Place_ID = place.pk
            place.save()
    
    return render(request, "neptune/pages/place_list.html", add_csrf(request, places=places,
                                                                        ))
''' View person profile. ''' 
def person_profile(request, id):
    #Article.objects.filter(publications=1)
    person = Person.objects.get(Person_ID=id)
    places = person.Places.all()
    
    return render(request, "neptune/pages/person_profile.html", add_csrf(request, person=person,
                                                                         places=places
                                                                        ))

''' View JSON person profile. ''' 
def person_profile_json(request, id):

    person = Person.objects.get(Person_ID=id)

    ''' Serialize "person" object for HTML output profile. '''
    serialized_obj = serializers.serialize('json', [ person, ])
    output = json.dumps(json.loads(serialized_obj), indent=4)
    return HttpResponse(output, content_type="application/json")

''' View JSON person profile. ''' 
def places_profile_json(request, id):

    person = Person.objects.get(Person_ID=id)
    places = person.Places.all()

    #leads_as_json = serializers.serialize('json', Lead.objects.all())
    ''' Serialize "place" object for HTML output profile. '''
    #serialized_obj = serializers.serialize('json', [ person, ])
    serialized_obj = serializers.serialize('json', places)
    output = json.dumps(json.loads(serialized_obj), indent=4)
    return HttpResponse(output, content_type="application/json")

''' View place profile. ''' 
def place_profile(request, id):

    place = Place.objects.get(Place_ID=id)
    
    return render(request, "neptune/pages/place_profile.html", add_csrf(request, place=place,
                                                                        ))
''' View JSON place profile. ''' 
def place_profile_json(request, id):

    place = Place.objects.get(Place_ID=id)
    ''' Serialize "place" object for HTML output profile. '''
    serialized_obj = serializers.serialize('json', [ place, ])
    output = json.dumps(json.loads(serialized_obj), indent=4)
    return HttpResponse(output, content_type="application/json")

''' Update place object with user values. ''' 
@login_required
def update_person(request, pk):

    '''Get requested instance of Place."'''  
    person = Person.objects.get(pk=pk)
    
    if request.method == "POST":
        pf = PersonForm(request.POST, request.FILES, instance=person) 
        if pf.is_valid():
            pf.save()
    else:
        pf = PersonForm(instance=person)

    return render(request, "neptune/pages/person_form.html", add_csrf(request, pf=pf,   
                                                     ))

''' Create or update profile waypoint with user values. ''' 
@login_required
def create_person(request):

    '''Form needs the "request.FILES" to upload files with form!'''
    if request.method == "POST":
        pf = PersonForm(request.POST) 
        if pf.is_valid():
            pf.save()
    else:
        pf = PersonForm()

    return render(request, "neptune/pages/person_form.html", add_csrf(request, pf=pf,   
                                                     ))

''' Update place object with user values. ''' 
@login_required
def update_place(request, pk):

    '''Get requested instance of Place."'''  
    place = Place.objects.get(pk=pk)
    
    if request.method == "POST":
        pf = PlaceForm(request.POST, instance=place) 
        #pf = LibraryForm(request.POST, request.FILES) 
        if pf.is_valid():
            pf.save()
    else:
        pf = PlaceForm(instance=place)
        #pf = LibraryForm()

    return render(request, "neptune/pages/place_form.html", add_csrf(request, pf=pf,   
                                                     ))

''' Create or update profile waypoint with user values. ''' 
@login_required
def create_place(request):
    ''' Create waypoint object from Waypoint model. ''' 
    #place = Place.objects.create()

    '''Form needs the "request.FILES" to upload files with form!'''
    GPS_alert = False
    if request.method == "POST":
        #pf = PlaceForm(request.POST, instance=place) 
        pf = PlaceForm(request.POST) 
        #if pf.is_valid() and ( (place.Compute_GPS and place.Address) or (place.Latitude and place.Longitude) ):
        if pf.is_valid():
            pf.save()
        else:
            '''Check if GPS fields are valid.'''
            if ( not ((place.Compute_GPS and place.Address) or (place.Latitude and place.Longitude)) ):
                GPS_alert = True
                
    else:
        pf = PlaceForm()

    return render(request, "neptune/pages/place_form.html", add_csrf(request, pf=pf,   
                                                     GPS_alert=GPS_alert
                                                     ))

def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

