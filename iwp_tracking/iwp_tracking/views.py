# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def index(request):
	return HttpResponse("index")
	return render_to_response('base.html')

def main_page(request):
	#return HttpResponse("main_page")
	return render_to_response('main/home.html')

def logout_page(request):
	logout(request)
	return render_to_response('index.html')