from django.shortcuts import render

from django.shortcuts import render_to_response
from django.forms import ModelForm
from classic.models import Calculation, CalculationAdmin
from django.core.context_processors import csrf
from django.core.exceptions import *

# Create your views here.
class CalculationForm(ModelForm):
    class Meta:
        model = Calculation
        # Include all fields.  
        fields = '__all__'
        # These fields are hidden to the user filling out the form.  
        #exclude = ["user", 'avatar_t', "posts", 'title_slug', "Country_slug", 'State_or_Province_slug']
        #fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
#         widgets = {
#             'address': Textarea(attrs={'cols': 50, 'rows': 1}),
#         }
        
def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

#def index(request):
#def experimental(request):
def stdform(request):
    #latest_calculation = Calculation.objects.last()
#     #latest_question = latest_calculation.question
#     pf = CalculationForm(instance=latest_calculation)
#     return render_to_response("index.html", add_csrf(request, pf=pf, latest_calculation=latest_calculation))
    # Example:  return render(request, 'polls/detail.html', {'question': question})
    #return render_to_response("index.html", add_csrf(request, pf=pf, {'question': latest_question}))
    #return render(request, "index.html", pf, {'question': latest_question})

    if request.method == "POST":
        pf = CalculationForm(request.POST) 
        if pf.is_valid():
            pf.save()
    else:
        pf = CalculationForm()

    last_calc = Calculation.objects.last()

    try:
            a = last_calc.A
    except AttributeError:
            a = 'A'

#     return render_to_response("stdform.html", add_csrf(request, pf=pf, a=a, 
#                                                      ))
    return render_to_response("stdform.html", add_csrf(request, pf=pf, a=a, 
                             last_calc=last_calc))

