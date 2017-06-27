from django.shortcuts import render
from django.http import HttpResponse
from collection.models import EyeImage, Survey, Profile
from collection.forms import ImageUploadForm
from django.conf import settings
from PIL import Image
from django.shortcuts import redirect
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
	#Get survey data
	if request.method == 'POST':
		mentalOptions = request.POST.getlist('mentalOptions')
		mental = 0
		for m in mentalOptions:
			mental += int(m)
		medicationOptions = request.POST.getlist('medicationOptions')
		medication = 0
		for m in medicationOptions:
			medication += int(m)
		medicationOther = request.POST.get('medicationOther')
		substancesOptions = request.POST.getlist('substancesOptions')
		substances = 0
		for s in substancesOptions:
			substances += int(s)
		if request.POST.get('otherOptions'):
			flash = int(request.POST.get('otherOptions'))
		else:
			flash = -1
		survey = Survey()
		imageId =  request.session.get('eye_image')
		survey.image = EyeImage.objects.get(id=imageId)
		survey.feelings = mental
		if request.POST.get('stateOptions'):
			survey.state = int(request.POST.get('stateOptions'))
		else:
			survey.state = -1
		survey.medications = str(medication) + medicationOther
		survey.substances = substances
		survey.flash = flash
		survey.save() 

	return render(request, 'collection/complete.html')


def faq(request):
	return render(request, 'collection/faq.html')

def consent(request):
	return render(request, 'collection/consent.html')

def survey(request):
	# x = float(request.POST['x_offset'])
	# y = float(request.POST['y_offset'])
	# width = float(request.POST['width'])
	# height = float(request.POST['height'])

	# right_low_x = x + width
	# right_low_y = y + height

	# eye_image = EyeImage(eye_image=request.FILES['file0'])
	# eye_image.participant = request.user
	# eye_image.image_id = 2
	# eye_image.image_name = request.FILES['file0'].name
	# eye_image.save()
	# request.session['eye_image'] = eye_image.id

	# #Crop image
	# im = Image.open(request.FILES['file0'])
	# if im.size[0] > im.size[1]:
	# 	im = im.rotate(-90)
	# box = (x, y, right_low_x, right_low_y)
	# cropped = im.crop(box)
	# cropped.save(settings.MEDIA_ROOT + '/crop/' + request.FILES['file0'].name, 'png')

	return render(request, 'collection/survey.html')

def profile(request):
	# #Get profile data
	if request.method == 'POST':
		age = int(request.POST.get('agerange'))
		gender = int(request.POST.get('gender'))
		diagnosis = int(request.POST.get('diagnosis'))
		profile = Profile()
		profile.user = request.user
		profile.age = age
		profile.gender = gender
		profile.diagnosis = diagnosis
		profile.save()
		return redirect('/collection/upload')

	return render(request, 'collection/profile.html')
