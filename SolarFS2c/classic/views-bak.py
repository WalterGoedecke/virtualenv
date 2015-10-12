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
class CalculationForm(ModelForm):
    class Meta:
        model = Calculation
        # Include all fields.  
        #fields = '__all__'
        # These fields are hidden to the user filling out the form.  
        #exclude = ["user", 'avatar_t', "posts", 'title_slug', "Country_slug", 'State_or_Province_slug']
        fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
        widgets = {
            'address': Textarea(attrs={'cols': 50, 'rows': 1}),
        }
        
# Test form.  
from django import forms
class CalcForm(forms.ModelForm):
    class Meta:
        model = Calculation
        # Include all fields.  
        #fields = '__all__'
        # These fields are hidden to the user filling out the form.  
        #exclude = ["user", 'avatar_t', "posts", 'title_slug', "Country_slug", 'State_or_Province_slug']
        fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
        widgets = {
            'address': Textarea(attrs={'cols': 50, 'rows': 1}),
            #'holiday_date': forms.DateInput(attrs={'class':'datepicker'}),
            'begin': forms.DateInput(attrs={'class':'datepicker'}),
        }
        
from classic.models import Holiday
class HolidayTimeForm(forms.ModelForm):

    class Meta:
        model = Holiday
        widgets = {
            'holiday_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

#def index(request):
#def experimental(request):
def stdform(request):

    if request.method == "POST":
        pf = CalculationForm(request.POST) 
        if pf.is_valid():
            pf.save()
    else:
        pf = CalculationForm()

    last_calc = Calculation.objects.last()
    address_slug = last_calc.address_slug

    # Time range output: formatt output by parsing every other comma. 
    # strChunks = [','.join(strArray[i:i+2]) for i in range(0, len(strArray), 2)]
#     t_seq = last_calc.time_sequence
#     t_seq_1 = t_seq.split('([')
#     #t_seq_begin = t_seq_1[0] + ':' # This is "DateTimeIndex:" label. 
#     t_seq_2 = t_seq_1[1].split('],')
#     #t_seq_end = t_seq_2[1]
#     t_seq_lines = t_seq_2[0].split(',') # Time data lines. 
#     t_seq_2lines = [','.join(t_seq_lines[i:i+2]) for i in range(0, len(t_seq_lines), 2)]

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
    # Test plot   
    # ---------------------------------------------------------  
    # Timestamp: 2012, 1, 1
    #d2 = [[1, 300], [2, 600], [3, 550], [4, 400], [5, 300]]
    # ---------------------------------------------------------  
    # End  test plot.  
    ############################  

    ############################  
    # Process the ephemeris data for plotting.   
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

    # Create the time-data array for the jquery plot. 
    len_eph = len(eph_seq_lines) # Number of data lines. 

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
    elif time_interval_hr <= 3: 
        tick_size = 20
        tick_unit = 'minute'
    elif time_interval_hr <= 5: 
        tick_size = 30
        tick_unit = 'minute'
    elif time_interval_hr < 8: 
        tick_size = 1
        tick_unit = 'hour'
    elif time_interval_hr <= 16: 
        tick_size = 2
        tick_unit = 'hour'
    elif time_interval_day <= 1: 
        tick_size = 4
        tick_unit = 'hour'
    elif time_interval_day <= 4: 
        tick_size = 12
        tick_unit = 'hour'
    else: # > 2 days. 
        tick_size = 1
        tick_unit = 'day'

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
    local_timezone_offset = time.altzone/3600 # Seconds to hours. 
    
    # Test variables.
    special = local_timezone_offset
    extraspecial = [tick_size, tick_unit]
    ####### End  ephemeris plotting. ######  

    return render_to_response("stdform.html", add_csrf(request, pf=pf, address_slug=address_slug, 
                                                     last_calc=last_calc, #time_sequence_lines=t_seq_2lines, 
                                                     #time_sequence_begin=t_seq_begin,  time_sequence_end=t_seq_end,
                                                     ephem_sequence_lines=eph_seq_lines, STATIC_URL=STATIC_URL, 
                                                     stat_lines=stat_lines, irrad_lines = irrad_lines, 
                                                     azimuth_data=azimuth_data, zenith_data=zenith_data, 
                                                     DHI_data=DHI_data, DNI_data=DNI_data, GHI_data=GHI_data, DB_data=DB_data, 
                                                     local_timezone=local_timezone, tick_size=tick_size, tick_unit=tick_unit,
                                                     special=special, extraspecial=extraspecial
                                                     ))

def SolarFSform(request):

    if request.method == "POST":
        pf = CalculationForm(request.POST) 
        pf_calc = CalcForm(request.POST) 
        if pf.is_valid():
            pf.save()
        if pf_calc.is_valid():
            pf_calc.save()
    else:
        pf = CalculationForm()
        pf_calc = CalcForm()

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
    # Process the ephemeris data for plotting.   
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

    # Create the time-data array for the jquery plot. 
    len_eph = len(eph_seq_lines) # Number of data lines. 

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
    local_timezone_offset = time.altzone/3600 # Seconds to hours. 
    
    # Test variables.
    special = [time_interval_hr, time_interval_day]
    extraspecial = [tick_size, tick_unit]
    ####### End  ephemeris plotting. ######  

    return render_to_response("SolarFSform.html", add_csrf(request, pf=pf, address_slug=address_slug, 
                                                     last_calc=last_calc, STATIC_URL=STATIC_URL, 
                                                     pf_calc=pf_calc, 
                                                     #time_sequence_lines=t_seq_2lines, 
                                                     #time_sequence_begin=t_seq_begin,  time_sequence_end=t_seq_end,
                                                     ephem_sequence_lines=eph_seq_lines, stat_lines=stat_lines, irrad_lines = irrad_lines, 
                                                     azimuth_data=azimuth_data, zenith_data=zenith_data, 
                                                     DHI_data=DHI_data, DNI_data=DNI_data, GHI_data=GHI_data, DB_data=DB_data, 
                                                     local_timezone=local_timezone, delta_time_hr=time_interval_hr, delta_time_day=time_interval_day,
                                                     tick_size=tick_size, tick_unit=tick_unit, time_format=time_format, axis_label=axis_label, 
                                                     special=special, extraspecial=extraspecial
                                                     ))



