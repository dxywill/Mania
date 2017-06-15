from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'collection/home.html')

def upload(request):
	return render(request, 'collection/upload.html')