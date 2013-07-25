from django.db import models
from django.contrib import admin
from django.utils import timezone
import datetime
import time
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
# Create your models here.


    #Actual Values
Red     = '#CD5555'
Blue    = '#BFEFFF'
Green   = '#A2C257'
Yellow  = '#FEE5AC'
Orange	= '#FF7F50'
Purple  = '#BDA0CB'
White 	= '#FFFFFF'


#What is Displayed in the Dropdown
COLORS = (
    (Red, 'Red'),
    (Blue, 'Blue'),
    (Yellow, 'Yellow'),
    (Orange, 'Orange'),
    (Green, 'Green'),
    (Purple, 'Purple'),
    (White, 'White'),

    )
#Font Colors
_Red     = 'red'
_Blue    = 'blue'
_Green   = 'green'
_Yellow  = 'yellow'
_Orange	= 'orange'
_Purple  = 'purple'
_Black	= 'black'

#What is Displayed in the Dropdown
FONT_COLORS = (
    (_Red, 'Red'),
    (_Blue, 'Blue'),
    (_Yellow, 'Yellow'),
    (_Orange, 'Orange'),
    (_Green, 'Green'),
    (_Purple, 'Purple'),
    (_Black, 'Black'),
    )
class Project(models.Model):
	Number = models.IntegerField(max_length = 10, primary_key = True)
	Name = models.CharField(max_length = 100)
	Contractor = models.ForeignKey('Contractor')
	Installer = models.ForeignKey('Installer')
	City = models.CharField(max_length = 100)
	State = USStateField(blank=True, null=True)


	def __unicode__(self):
		Display = str(self.Number)+" - "+self.Name + " - " + self.Contractor.Abr
		return unicode(Display)

class Contractor(models.Model):
	Name = models.CharField(max_length = 100)
	Abr = models.CharField(max_length = 10)
	

	def __unicode__(self):
		#Display = self.JobNumber+" - "+self.JobName 
		return unicode(self.Abr)

class Installer(models.Model):
	Name = models.CharField(max_length = 100)
	

	def __unicode__(self):
		#Display = self.JobNumber+" - "+self.JobName 
		return unicode(self.Name)

class WorkOrder(models.Model):
	Number 			= 		 models.IntegerField(max_length = 10, primary_key = True)
	ProjectNumber	= 		 models.ForeignKey('Project')
	Description		=		 models.CharField(max_length = 100)
	Engineer 		=		 models.ForeignKey('Engineer')
	Shipped 		=		 models.BooleanField(default = False)
	ShipDate		=		 models.DateField(default = datetime.datetime.now())
	Batch 			=		 models.CharField(max_length = 20)
	BoxCount		=		 models.IntegerField(max_length= 4)
	Notes 			=		 models.TextField()
	ReleaseToShop 	=	 	 models.DateField(default = datetime.datetime.now())
	Future 			= 		 models.BooleanField(default = True)
	Driver			= 		 models.ForeignKey('Driver')
	TxtColor 		= 		 models.CharField(max_length = 7, choices = FONT_COLORS, default = _Black)
	BkgrdColor		=		 models.CharField(max_length = 7, choices = COLORS, default = White)
	def __unicode__(self):
		Display = str(self.Number)+" - "+self.Description+" - "+str(self.ProjectNumber)
		return unicode(Display)
	def shipbool(self):
		if self.Shipped: 
			return "True"
		else:
			return "False"

	def futurebool(self):
		if self.Future: 
			return "True"
		else:
			return "False"
class Engineer(models.Model):
	user	 = models.OneToOneField(User) #changed from foreign key user.
	Initials =	models.CharField(max_length = 3)
	def __unicode__(self):
		#Display = self.JobNumber+" - "+self.JobName 
		return unicode(self.Initials)

class Driver(models.Model):
	Name = models.CharField(max_length = 20)
	def __unicode__(self):
		#Display = self.JobNumber+" - "+self.JobName 
		return unicode(self.Name)

admin.site.register(WorkOrder)
admin.site.register(Engineer)
admin.site.register(Installer)
admin.site.register(Project)
admin.site.register(Contractor)
admin.site.register(Driver)

