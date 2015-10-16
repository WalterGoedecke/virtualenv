from django.db import models
from django.contrib import admin

# Create your models here.

class MyProfile(models.Model):
    user = models.OneToOneField("auth.User")
    #date_of_birth = models.DateField()
    bio = models.TextField()

class Calculation(models.Model):
    A = models.CharField(max_length=80, blank=True, null=True, default='A')
    B = models.CharField(max_length=80, blank=True, null=True, default='B')
    
    def __str__(self):
        #return self.A
        return '%s %s' % (self.A, self.B)

    def process(self, A):
        self.B  = A
        return self.B

    def save(self, *args, **kwargs):
        self.process(self.A)
        # Save all. 
        super(Calculation, self).save()

class CalculationAdmin(admin.ModelAdmin):
    search_fields = ["A"]
    display_fields = ["A"]


