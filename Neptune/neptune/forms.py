from django import forms
from django.forms import ModelForm, Textarea
from neptune.models import User, Person, Place

''' User account profile form. ''' 
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         '''Include all fields.'''  
#         fields = '__all__'
#         '''These fields are hidden to the user filling out the form.'''  
#         exclude = ["Geo_Marker", 'Label', "Content", 'Pix_1', "Pix_2"]
        
''' User form for person. ''' 
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        '''Include all fields.'''  
        fields = '__all__'
        '''These fields are hidden to the user filling out the form.'''  
        #exclude = ["Person_ID"]
        #fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
        '''Pick fields.''' 
        #fields = ['Other_websites']
        
''' User form for place. ''' 
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        '''Include all fields.'''  
        fields = '__all__'
        '''These fields are hidden to the user filling out the form.'''  
        #exclude = ["Place_ID"]
        #fields = ['address', 'begin', 'end', 'frequency', 'panel_azimuth', 'panel_tilt']
        #widgets = {
        #    'address': Textarea(attrs={'cols': 50, 'rows': 1}),
        #}
        '''Pick fields.''' 
        #fields = ['Other_websites']
        
class ChoiceForm(forms.Form):
    GeoJunk = forms.BooleanField(required=False, initial=True)
    Little_Free_Library = forms.BooleanField(required=False, initial=True)
    Garage_Sale = forms.BooleanField(required=False, initial=True)
     
    '''Hidden character field to hold JQuery slider value.'''
    slider_field = forms.CharField(max_length=4, required=False)
    
    #def __init__(self, *args, **kwargs):
        #super(MyModelForm, self).__init__(*args, **kwargs)
    #    form.slider_value.widget = forms.HiddenInput()

