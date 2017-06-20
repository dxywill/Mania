from django.shortcuts import render
from django.http import HttpResponse
from collection.models import EyeImage
from collection.forms import ImageUploadForm

# Create your views here.

def landing(request):
	return render(request, 'collection/landing.html')

def index(request):
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			eye_image = EyeImage(eye_image=request.FILES['image'])
			eye_image.participant = request.user
			eye_image.image_id = 2
			eye_image.save()
			context_data = {'image': eye_image }
			return render(request, 'collection/upload.html', context_data)
			
	return render(request, 'collection/home.html')

def upload(request):
	return render(request, 'collection/upload.html')

def complete(request):
	x = request.POST['x_offset']
	y = request.POST['y_offset']
	width = request.POST['width']
	height = request.POST['height']

	context_data = {
		"x" : x,
		"y" : y,
		"width" : width,
		"height": height
	}
	print(context_data)
	return render(request, 'collection/complete.html', context_data)


def faq(request):
	return render(request, 'collection/faq.html')

def consent(request):
	return render(request, 'collection/consent.html')