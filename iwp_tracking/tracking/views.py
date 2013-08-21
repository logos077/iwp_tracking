# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.core.context_processors import csrf
from django.template import RequestContext
from tracking.models import *
from tracking.forms import *

def check_permissions(user):
    var1 = user.groups.filter(name ='Admin').exists()
    
    var2 = user.groups.filter(name ='Engineer').exists()
    if var1 or var2 ==True:
        result = True
    else:
        result = False
    return result


@login_required
def tracking(request):
	
	this_list = WorkOrder.objects.filter(Shipped = False, Future = False).order_by("ShipDate", "ProjectNumber")
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
	
	return response


@login_required
def search(request):
	found_entries = None
	query_string = ''
	found_entry = None
	search_exists = False
	error_message = ""
	this_list = WorkOrder.objects.filter(Shipped = False, Future = order_by).False("ShipDate", "ProjectNumber")
	context = {'this_list':this_list}
	template_name = "tracking/tracking_main.html"
	response = render_to_response(template_name,context,RequestContext(request))
	
	if ('q' in request.GET) and request.GET['q'].strip():
		
		query_string = request.GET['q']
		try:
			job_number = int(query_string)

		except ValueError:
			error_message = " Value Error not a Number"#return HttpResponse("ValueError")
			job_number = 0

		
		found_entry = Project.objects.get(Number = job_number)
		found_entries = Project.objects.filter(Number = job_number)
  		
		if found_entries.exists():
			this_list = WorkOrder.objects.filter(ProjectNumber = found_entry.id).order_by("ShipDate", "ProjectNumber")
			context = {'this_list':this_list}
			#return HttpResponse(found_entry.Number)
			template_name = "tracking/tracking_main.html"
			response = render_to_response(template_name,context,RequestContext(request))
		
		else:
			message = "JOB NOT FOUND!"
			context = {'this_list':this_list, "message":message, "error_message":error_message}
			response = render_to_response(template_name,context,RequestContext(request))

	return response
@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def new_project(request):
	
	form = NewProjectForm
	context = {'form':form}
	template_name = "tracking/new_project.html"
	success_template = "tracking/success.html"
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
@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def new_work_order(request):
	pk = request.user.id
	en = Engineer.objects.get(user=pk)
	form = NewWOForm()
	form.initial['Engineer'] = en
	context = {'form':form}
	template_name = "tracking/new_work_order.html"
	success_template = "tracking/success.html"
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
			
			context = {'form':form}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response
@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def edit_work_order(request, pk):
	wo_id = int(pk)
	#wo_number = int(pk)
	wo = WorkOrder.objects.get(pk = wo_id)
	form = NewWOForm()
	
	template_name = "tracking/new_work_order.html"
	success_template = "tracking/success.html"
	
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
			wof.id = wo.id
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
			
			context = {'form':form}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response


@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def new_driver(request):
	form = NewDriverForm
	drivers = Driver.objects.all()
	title = "New Driver"
	context_message = "Enter New Driver"
	context = {'form':form, 'drivers':drivers, 'title':title,'context_message':context_message}
	template_name = "tracking/new_driver.html"
	success_template = "tracking/success.html"
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewDriverForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(success_template,RequestContext(request))
		else:
			
			context = {'form':form, 'drivers':drivers, 'title':title,'context_message':context_message}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response

@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def new_installer(request):
	form = NewInstallerForm
	installers = Installer.objects.all()
	
	template_name = "tracking/new_installer.html"
	success_template = "tracking/success.html"
	title = "New Installer"
	context_message = "Enter New Installer:"
	context = {'form':form, 'installers':installers, 'title':title,'context_message':context_message}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewInstallerForm(request.POST)
		if form.is_valid():
			form.save()
			template_name = success_template
			response = render_to_response(template_name, context,RequestContext(request))
		else:
			
			context = {'form':form, 'installers':installers,'title':title,'context_message':context_message}
			response = render_to_response(template_name,context,RequestContext(request))
	
	return response


@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def new_contractor(request):
	form = NewContractorForm()
	contractors = Contractor.objects.all()
	count = Contractor.objects.all().count()
	
	message = "New Contractor"
	template_name = "tracking/new_contractor.html"
	success_template = "tracking/new_contractor.html"
	context = {'form':form, 'contractors':contractors, 'count':count, 'message':message}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewContractorForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			
			context = {'form':form, 'contractors':contractors, 'count':count, 'message':message}
			response = render_to_response(template_name,context,RequestContext(request))
	elif request.method == 'GET':
		
		query_string = ''
		found_entries = None
		if ('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			found_entries = Contractor.objects.filter(Name__icontains = query_string).order_by('Name')
			
			search_exists = found_entries.exists()

			response =  render_to_response('tracking/con_search_results.html',
			{ 'query_string': query_string, 'found_entries': found_entries, 'search_exists': search_exists },
			context_instance=RequestContext(request))






	return response

@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def edit_con(request, pk):
	string = pk
	con_id = int(pk)
	form = NewContractorForm()
	contractors = Contractor.objects.all()
	count = Contractor.objects.all().count()
	title = "Edit Contractor"
	context_message =  "Enter New Driver to add:"

	
	
	this_Contractor = Contractor.objects.get(pk =con_id)
	form.initial['Name'] = this_Contractor.Name
	form.initial['Abr'] = this_Contractor.Abr
	

	template_name = "tracking/new_contractor.html"
	context = {'form':form, 'contractors':contractors, 'count':count, 'title':title,'context_message':context_message}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewContractorForm(request.POST, instance = this_Contractor)
		
		
		response = render_to_response(template_name,context,RequestContext(request))
		if form.is_valid():
			success_template = "tracking/tracking_main.html"
			ecf= form.save(False)
			ecf.id = con_id
			ecf.Name = this_Contractor.Name
			ecf.Abr = this_Contractor.Abr
			ecf.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'contractors':contractors, 'count':count, 'title':title,'context_message':context_message}
			response = render_to_response(template_name,context,RequestContext(request))

	#response = HttpResponse(string)
	return response

@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def edit_driver(request, pk):
	string = pk
	drv_id = int(pk)
	form = NewDriverForm()
	title = "Edit Driver"
	context_message = title
	
	this_Driver = Driver.objects.get(pk = drv_id)
	form.initial['Name'] = this_Driver.Name
	
	

	template_name = "tracking/new_driver.html"
	context = {'form':form, 'title':title, 'context_message':context_message}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewDriverForm(request.POST, instance = this_Driver)
		
		
		response = render_to_response(template_name,context,RequestContext(request))
		if form.is_valid():
			success_template = "tracking/tracking_main.html"
			edf= form.save(False)
			edf.id = drv_id
			edf.Name = this_Driver.Name
			edf.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'title':title, 'context_message':context_message}
			response = render_to_response(template_name,context,RequestContext(request))

	#response = HttpResponse(string)
	return response


@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def edit_installer(request, pk):
	string = pk
	drv_id = int(pk)
	form = NewInstallerForm()
	title = "Edit Installer"
	context_message = title
	
	this_Installer = Installer.objects.get(pk =drv_id)
	form.initial['Name'] = this_Installer.Name

	template_name = "tracking/new_installer.html"
	context = {'form':form, 'title':title, 'context_message':context_message}
	response = render_to_response(template_name,context,RequestContext(request))
	if request.method == 'POST':
		form = NewInstallerForm(request.POST, instance = this_Installer)
		
		
		response = render_to_response(template_name,context,RequestContext(request))
		if form.is_valid():
			success_template = "tracking/tracking_main.html"
			edf= form.save(False)
			edf.id = drv_id
			edf.Name = this_Installer.Name
			edf.save()
			response = render_to_response(template_name,RequestContext(request))
		else:
			#return HttpResponse("not Valid")
			context = {'form':form, 'title':title, 'context_message':context_message}
			response = render_to_response(template_name,context,RequestContext(request))

	#response = HttpResponse(string)
	return response

@login_required
@user_passes_test(check_permissions, login_url ="/main/access_denied/")
def tracking_log(request):
	title = "Tracking Log"
	lst = []
	this_list = lst[:20]
	
	template_name = "tracking/tracking_log.html"
	context = {'this_list':this_list}
	response = render_to_response(template_name,context,RequestContext(request))


	#response = HttpResponse(string)
	return response