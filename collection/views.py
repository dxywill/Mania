from django.shortcuts import render
from django.http import HttpResponse
from collection.models import EyeImage
from collection.forms import ImageUploadForm

# Create your views here.

def index(request):
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			eye_image = EyeImage(eye_image=request.FILES['image'])
			eye_image.participant = request.user
			eye_image.image_id = 2
			eye_image.save()
			return HttpResponse('image upload success')
	return render(request, 'collection/home.html')

def upload(request):
	return render(request, 'collection/upload.html')