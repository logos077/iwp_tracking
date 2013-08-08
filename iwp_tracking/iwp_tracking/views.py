# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext

def index(request):
	
	return render_to_response('index.html')

def main_page(request):
	#return render_to_response('main/home.html')
	return render_to_response('main/home.html',RequestContext(request))

def logout_page(request):
	logout(request)
	return render_to_response('index.html')

def access_denied(request):
	return render_to_response('main/access_denied.html')