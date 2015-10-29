#from django.shortcuts import render

from django.shortcuts import render_to_response
#from django.forms import ModelForm
from classic.models import Calculation #, CalculationAdmin
from django.core.context_processors import csrf
from django.core.exceptions import *

# Make home page editable.
from mezzanine.pages.views import page  

from SolarFS2c.settings import STATIC_URL
from django.forms import ModelForm, Textarea

import datetime, time # Convert year, month, day, &c., to seconds since 1970. 
from dateutil.tz import * # For local time zone determination. 
# Create your views here.

# Make home page editable.
def home_page(request):
    # Links to: url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
    # Not needed. 
    request.path = "/" 
    return page(request, "home")

# ModelForm must be in views, not model. 
from django import forms

class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        # Include all fields.  
        #fields = '__all__'
        # These fields are hidden to the user filling out the form.  
        #exclude = ["user", 'avatar_t', "posts", 'title_slug', "Country_slug", 'State_or_Province_slug']
        fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
        widgets = {
            'address': Textarea(attrs={'cols': 50, 'rows': 1}),
#             'begin': forms.DateInput(attrs={'class':'datetimepicker'}),
#             'end': forms.DateInput(attrs={
#                                           'class':'datetimepicker'
#                                           #'minDate': "$("#begin").datepicker("getDate")"
#             }),
        }
        
def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

def SolarFSform(request):

    if request.method == "POST":
        pf = CalculationForm(request.POST) 
        if pf.is_valid():
            pf.save()
    else:
        pf = CalculationForm()

    last_calc = Calculation.objects.last()
    address_slug = last_calc.address_slug

    # Solar ephemeris. 
    eph_seq = last_calc.ephem_sequence
    eph_seq_lines = eph_seq.split('\n')[1:] #Trim first label line. 

    # Statistics. 
    stats = last_calc.statistics
    stat_lines = stats.split('\n')
    
    # Irradiance. 
    irrad = last_calc.irradiance_sequence
    irrad_lines = irrad.split('\n')[1:] #Trim first label line.
    
    ############################  
    # Process the ephemeris and irradiance data.
    # ---------------------------------------------------------  
    # Initiate the string arrays. 
    strDateArray = [] 
    strTimeArray = [] 
    strAzimuthArray = [] 
    strZenithArray = [] 
    azimuth_data = []
    zenith_data = []

    strDHIarray = [] 
    strDNIarray = [] 
    strGHIarray = [] 
    strDBarray = [] 
    DHI_data = [] 
    DNI_data = [] 
    GHI_data = [] 
    DB_data = [] 

    len_eph = len(eph_seq_lines) # Number of data lines. 

    # Split the line apart to get the date & time, and then split the UTC time off at the end, 
    #  e.g., "2015-07-01 11:00:00-06:00 93.772828 40.178462" 
    # Also create string arrays of the solar azimuth & zeniths, the 3rd & 4th values. 
    for line in eph_seq_lines: 
        line_parts = line.split() #Split line on spaces. 
        strDate = line_parts[0].split('-')
        strDateArray.append(strDate)
        strTime = line_parts[1].split('-')[0].split(':')
        strTimeArray.append(strTime)
        strAzimuthArray.append(line_parts[2]) # Azimuth of sun. 
        strZenithArray.append(line_parts[3]) # Zenith, or elevatgion of sun.  # Error 1

    for line in irrad_lines: 
        line_parts = line.split() #Split line on spaces. 
        strDHIarray.append(line_parts[2]) # Azimuth of sun. 
        strDNIarray.append(line_parts[3]) # Azimuth of sun. 
        strGHIarray.append(line_parts[4]) # Azimuth of sun. 
        strDBarray.append(line_parts[5]) # Azimuth of sun. 

    # Create a float array from the string list.  
    fltAzimuthArray = [float(s) for s in strAzimuthArray]    # Error 2
    fltZenithArray = [float(s) for s in strZenithArray]  
        
    fltDHIarray = [float(s) for s in strDHIarray]  
    fltDNIarray = [float(s) for s in strDNIarray]  
    fltGHIarray = [float(s) for s in strGHIarray]  
    fltDBarray = [float(s) for s in strDBarray]  

    # Return the milliseconds since 1970 from the year, month, day, hour, minute, & second. 
    # Append the ephemeris data to the millisecond epoch time stamp. 
    for i in range(len_eph - 1):
        # Returns the unix time stamp, the seconds since midnight, New Year's Day, 1970, UTC.  
        # This implies that the local time is converted to UTC time within function. 
        dt = datetime.datetime( int(strDateArray[i][0]), int(strDateArray[i][1]), int(strDateArray[i][2]), 
                             int(strTimeArray[i][0]), int(strTimeArray[i][1]), int(strTimeArray[i][2]) )
        s = 1000*time.mktime(dt.timetuple()) # Milliseconds since 1970. 
        azimuth_data.append([s, fltAzimuthArray[i]])
        zenith_data.append([s, fltZenithArray[i]])

        DHI_data.append([s, fltDHIarray[i]])
        DNI_data.append([s, fltDNIarray[i]])
        GHI_data.append([s, fltGHIarray[i]])
        DB_data.append([s, fltDBarray[i]])

    # This is the local time zone, e.g., "MDT." 
    local_timezone = datetime.datetime.now(tzlocal()).tzname()
    # Offset from UTC to local time in hours, e.g., UTC - local_timezone_offset = local time. 
    #local_timezone_offset = time.altzone/3600 # Seconds to hours. 
    ####### End  data processing.  #######  
    
    ############################  
    # Process the data for plotting.   
    # ---------------------------------------------------------  
    # Create the time-data array for the jquery plot. 
    # Calculate time interval from begin to end in hours. . 
    dt = datetime.datetime( int(strDateArray[0][0]), int(strDateArray[0][1]), int(strDateArray[0][2]), 
                         int(strTimeArray[0][0]), int(strTimeArray[0][1]), int(strTimeArray[0][2]) )
    s_begin = time.mktime(dt.timetuple()) # Milliseconds since 1970. 
    dt = datetime.datetime( int(strDateArray[len_eph-1][0]), int(strDateArray[len_eph-1][1]), int(strDateArray[len_eph-1][2]), 
                         int(strTimeArray[len_eph-1][0]), int(strTimeArray[len_eph-1][1]), int(strTimeArray[len_eph-1][2]) )
    s_end = time.mktime(dt.timetuple()) # Milliseconds since 1970. 
    time_interval_hr = (s_end - s_begin)/3600 
    time_interval_day = time_interval_hr/24 
    
    # Calculate the plot tick size in minutes for an optimal x-plot scale. 
    if time_interval_hr <= 1: # Hour. 
        tick_size = 10 #[10, "minute"]
        tick_unit = 'minute'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_hr <= 3: 
        tick_size = 20
        tick_unit = 'minute'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_hr <= 5: 
        tick_size = 30
        tick_unit = 'minute'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_hr <= 10: 
        tick_size = 1
        tick_unit = 'hour'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_hr <= 24: 
        tick_size = 2
        tick_unit = 'hour'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_day <= 3: 
        tick_size = 6
        tick_unit = 'hour'
        time_format = "%H:%M"
        axis_label = "hr:min"
    elif time_interval_day <= 4: 
        tick_size = 12
        tick_unit = 'hour'
        time_format = "%m-%d %H"
        axis_label = "mo-day hr"
    else: # > 2 days. 
        tick_size = 1
        tick_unit = 'day'
        time_format = "%m-%d"
        axis_label = "mo-day"
    ####### End  plotting preparation.  #######  
        
    ############################  
    # Process the data arrays for display.   
    # ---------------------------------------------------------  
    # Create an array to display to the screen; if the array is greater than 40 lines, 
    #    display only ellipsis (...) in the middle. 
    len_eph = len(eph_seq_lines) # Number of data lines. 

    ephem_sequence_lines = [] 
    irradiance_lines = [] 
    if len_eph > 40:
        # Ephemeris data. 
        for line in eph_seq_lines[0:19]:
            ephem_sequence_lines.append(line)
        ephem_sequence_lines.append('...') 
        for line in eph_seq_lines[len_eph-20:len_eph]:
            ephem_sequence_lines.append(line)
        # Irradiance data. 
        for line in irrad_lines[0:19]:
            irradiance_lines.append(line)
        irradiance_lines.append('...') 
        for line in irrad_lines[len_eph-20:len_eph]:
            irradiance_lines.append(line)
    
    ####### End  display preparation.  #######  
        
    # Test variables.
    #special = [time_interval_hr, time_interval_day]
    #special = local_timezone_offset
    special = len_eph
    #extraspecial = [tick_size, tick_unit]
    extraspecial = eph_seq_lines[0]
    
    return render_to_response("SolarFSform.html", add_csrf(request, pf=pf, address_slug=address_slug, 
                                                     last_calc=last_calc, STATIC_URL=STATIC_URL, 
                                                     ephem_sequence_lines=ephem_sequence_lines, stat_lines=stat_lines, irradiance_lines=irradiance_lines, 
                                                     azimuth_data=azimuth_data, zenith_data=zenith_data, 
                                                     DHI_data=DHI_data, DNI_data=DNI_data, GHI_data=GHI_data, DB_data=DB_data, 
                                                     local_timezone=local_timezone, delta_time_hr=time_interval_hr, delta_time_day=time_interval_day,
                                                     tick_size=tick_size, tick_unit=tick_unit, time_format=time_format, axis_label=axis_label, 
                                                     special=special, extraspecial=extraspecial
                                                     ))



