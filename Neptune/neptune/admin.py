from django.contrib import admin

# Register your models here.
from neptune.models import Person, Place

admin.site.register(Person)
admin.site.register(Place)
