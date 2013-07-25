# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.core.context_processors import csrf
from django.template import RequestContext
from tracking.models import *
from tracking.forms import *

def tracking(request):
	
	this_list = WorkOrder.objects.filter(Shipped = False).order_by("ShipDate", "ProjectNumber")
	model = WorkOrder
	context = {'this_list':this_list}
	template_name = "tracking/tracking_main.html"
	response = render_to_response(template_name,context,RequestContext(request))
	
	if request.method =="POST":
		job_filter = request.POST['job_filter']
		
		if job_filter == 'Future':
			this_list = WorkOrder.objects.filter(Future = True).order_by("ShipDate")
			context = {'this_list':this_list}
			response = render_to_response(template_name,context,RequestContext(request))

		elif job_filter == 'Shipped':
			this_list = WorkOrder.objects.filter(Shipped =True).order_by("ShipDate")
			context = {'this_list':this_list}
			response = render_to_response(template_name,context,RequestContext(request))

		elif job_filter == 'All':
			this_list = WorkOrder.objects.all().order_by("ShipDate", "ProjectNumber")
			context = {'this_list':this_list}
			response = render_to_response(template_name,context,RequestContext(request))



		#return HttpResponse(job_filter)
	
	
	return response

def search(request):
	query_string = ''
	found_entries = None
	search_exists = False
	this_list = WorkOrder.objects.filter(Shipped = False).order_by("ShipDate", "ProjectNumber")
	context = {'this_list':this_list}
	template_name = "tracking/tracking_main.html"
	response = render_to_response(template_name,context,RequestContext(request))
	
	if ('q' in request.GET) and request.GET['q'].strip():
		
		query_string = request.GET['q']
		job_number = int(query_string)
		found_entries = Project.objects.filter(Number = job_number)
  		
		if found_entries.exists():
			this_list = WorkOrder.objects.filter(ProjectNumber = job_number).order_by("ShipDate", "ProjectNumber")
			context = {'this_list':this_list}
			template_name = "tracking/tracking_main.html"
			response = render_to_response(template_name,context,RequestContext(request))
		else:
			#this_list = WorkOrder.objects.filter(Shipped = False).order_by("ShipDate", "ProjectNumber")
			#context = {'this_list':this_list}
			#template_name = "tracking/tracking_main.html"
			message = "JOB NOT FOUND!"
			context = {'this_list':this_list, "message":message}
			response = render_to_response(template_name,context,RequestContext(request))

	return response 
def new_project(request):
	
	form = NewProjectForm
	context = {'form':form}
	template_name = "tracking/new_project.html"
	success_template = "/main/"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == "POST":
		form = NewProjectForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(success_template,RequestContext(request))
		else:
			context = {'form':form}
			response = render_to_response(template_name,context,RequestContext(request))
	


	
	return response

def new_work_order(request):
	

	form = NewWOForm
	context = {'form':form}
	template_name = "tracking/new_work_order.html"
	success_template = "/main/"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewWOForm(request.POST)
		if form.is_valid():
			form.save()
			this_list = WorkOrder.objects.all().order_by("ShipDate", "ProjectNumber")
			model = WorkOrder
			context = {'this_list':this_list}
			template_name = "tracking/tracking_main.html"
			response = render_to_response(template_name,context,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response

def edit_work_order(request, pk):
	wo_number = int(pk)
	wo = WorkOrder.objects.get(Number = wo_number)
	form = NewWOForm()
	
	template_name = "tracking/new_work_order.html"
	success_template = "/main"
	
	form.initial['Number'] = wo.Number
	form.initial['ProjectNumber'] = wo.ProjectNumber
	form.initial['Description'] = wo.Description
	form.initial['Engineer'] = wo.Engineer
	form.initial['Shipped'] = wo.Shipped
	form.initial['ShipDate'] = wo.ShipDate
	form.initial['Batch'] = wo.Batch
	form.initial['BoxCount'] = wo.BoxCount
	form.initial['Notes'] = wo.Notes
	form.initial['ReleaseToShop'] = wo.ReleaseToShop
	form.initial['Future'] = wo.Future
	form.initial['Driver'] = wo.Driver
	form.initial['TxtColor'] = wo.TxtColor
	form.initial['BkgrdColor'] = wo.BkgrdColor
	context = {'form':form}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewWOForm(request.POST, instance = wo)
		if form.is_valid():
			success_template = "tracking/tracking_main.html"
			wof =form.save(False)
			
			wof.Number = wo.Number
			wof.ProjectNumber = wo.ProjectNumber
			wof.Description= wo.Description
			wof.Engineer= wo.Engineer
			wof.Shipped = wo.Shipped
			wof.ShipDate= wo.ShipDate
			wof.Batch= wo.Batch
			wof.BoxCount= wo.BoxCount
			wof.Notes= wo.Notes
			wof.ReleaseToShop = wo.ReleaseToShop
			wof.Future = wo.Future
			wof.Driver= wo.Driver
			wof.TxtColor= wo.TxtColor
			wof.BkgrdColo= wo.BkgrdColor 
			wof.save()
			this_list = WorkOrder.objects.all().order_by("ShipDate", "ProjectNumber")
			model = WorkOrder
			context = {'this_list':this_list}
			template_name = "tracking/tracking_main.html"
			response = render_to_response(template_name,context,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response
def new_driver(request):
	form = NewDriverForm
	drivers = Driver.objects.all()
	context = {'form':form, 'drivers':drivers}
	template_name = "tracking/new_driver.html"
	success_template = "/main/"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewDriverForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'drivers':drivers}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response


def new_installer(request):
	form = NewInstallerForm
	installers = Installer.objects.all()
	context = {'form':form, 'installers':installers}
	template_name = "tracking/new_installer.html"
	success_template = "/main/"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewInstallerForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'installers':installers}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response

def new_contractor(request):
	form = NewContractorForm
	contractors = Contractor.objects.all()
	context = {'form':form, 'contractors':contractors}

	template_name = "tracking/new_contractor.html"
	success_template = "tracking/new_contractor.html"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewContractorForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'contractors':contractors}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response

def main_page(request):
	#return HttpResponse("main_page")
	return render_to_response('main/home.html')