from django.shortcuts import render
from django.http import HttpResponse
from collection.models import EyeImage, Survey, Profile
from collection.forms import ImageUploadForm
from django.conf import settings
from PIL import Image
from django.shortcuts import redirect
import time

import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import boto3

# Create your views here.

def landing(request):
	#return render(request, 'collection/landing_new.html')
	return redirect('/accounts/login/')

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


def encrypt(key, filename):
    chunk_size = 64*1024
    output_file = filename+".enc"
    file_size = str(os.path.getsize(filename)).zfill(16)
    IV = ''
    for i in range(16):
        IV += chr(random.randint(0, 0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, IV.encode("latin-1"))
    with open(filename, 'rb') as inputfile:
        with open(output_file, 'wb') as outf:
            outf.write(file_size.encode("latin-1"))
            outf.write(IV.encode("latin-1"))
            while True:
                chunk = inputfile.read(chunk_size)
                chunk = chunk
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                   chunk += b' '*(16 - len(chunk)%16)
                outf.write(encryptor.encrypt(chunk))

def survey(request):
	x = float(request.POST['x_offset'])
	y = float(request.POST['y_offset'])
	width = float(request.POST['width'])
	height = float(request.POST['height'])

	right_low_x = x + width
	right_low_y = y + height


	ts = str(time.time())

	request.FILES['file0'].name = request.user.username + '_' + ts + '.png'
	eye_image = EyeImage(eye_image=request.FILES['file0'])
	eye_image.participant = request.user
	eye_image.image_id = 2
	eye_image.image_name = request.user.username + '_' + ts + '.png'
	eye_image.save()
	request.session['eye_image'] = eye_image.id

	#Crop image
	im = Image.open(request.FILES['file0'])
	if im.size[0] > im.size[1]:
		im = im.transpose(Image.ROTATE_270)
	box = (x, y, right_low_x, right_low_y)

	cropped = im.crop(box)
	crop_path = settings.MEDIA_ROOT + '/crop/' + request.user.username + '_' + ts + '_crop.png'
	cropped.save(crop_path, 'png')

	rt_path = 'crop/' + request.user.username + '_' + ts + '_crop.png'
	eye_image_crop = EyeImage(eye_image=rt_path)
	eye_image_crop.participant = request.user
	eye_image_crop.image_id = 3
	eye_image_crop.image_name = request.user.username + '_' + ts + '_crop.png'
	eye_image_crop.save()

	#encrypt the image
	password = "theImagePassword$"
	hasher = SHA256.new(password.encode("latin-1"))
	digest = hasher.digest()
	filename = crop_path
	encrypt(digest, filename)

	#upload to S3
	s3 = boto3.client(
    	's3',
    	# Hard coded strings as credentials, not recommended. Change it when deploy.
    	aws_access_key_id='AKIAI3SCUO2NFTG4QGMQ',
    	aws_secret_access_key='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'
	)

	filename = crop_path
	bucket_name = 'smu-mania-study-images'
	s3.upload_file(filename, bucket_name, 'images/{}'.format(request.user.username + '_' + ts + '_crop.png'))

	return render(request, 'collection/survey.html')

def profile(request):
	#Get profile data
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
