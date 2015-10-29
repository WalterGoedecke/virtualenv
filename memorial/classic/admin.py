#from django.contrib import admin

# Register your models here.
#from mezzanine.pages.admin import PageAdmin
#from .models import DocPage

from classic.models import *

admin.site.register(Calculation, CalculationAdmin)

