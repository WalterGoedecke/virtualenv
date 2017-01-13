from django.conf.urls import patterns, url
from neptune.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('neptune.views',
    url(r"^person-list/$", person_list, name="person_list"),    
    url(r"^place-list/$", place_list, name="place_list"),    
    url(r"^person-profile/(\w+)/$", person_profile, name="person_profile"),    
    url(r"^place-profile/(\w+)/$", place_profile, name="place_profile"),    

    url(r"^place-profile-json/(\w+)/$", place_profile_json, name="place_profile_json"),    
    url(r"^person-profile-json/(\w+)/$", person_profile_json, name="person_profile_json"),    
    url(r"^places-profile-json/(\w+)/$", places_profile_json, name="places_profile_json"),    

    url("^update-person/(\w+)/$", update_person, name="update_person"),
    url("^create-person/$", create_person, name="create_person"),
    url("^update-place/(\w+)/$", update_place, name="update_place"),
    url("^create-place/$", create_place, name="create_place"),

    url("^$", person_list, name="person_list"),
) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
