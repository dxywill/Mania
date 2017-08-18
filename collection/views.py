from django.shortcuts import render
from django.http import HttpResponse
from collection.models import EyeImage, Survey, Profile
from collection.forms import ImageUploadForm
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import time
from datetime import datetime
from PIL import Image, ExifTags
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

def session(request):
    session_id = request.session.session_key
    s = Session.objects.get(pk=session_id)
    expired = 0
    expired_time = int(time.mktime(s.expire_date.timetuple()))
    current_time = int(time.mktime(datetime.utcnow().timetuple()))
    if expired_time < current_time:
        expired = 1

    return HttpResponse(expired)

@login_required
def upload(request):
    return render(request, 'collection/upload.html')

@login_required
def complete(request):
    #Get survey data
    if request.method == 'POST':
      
        imageId =  request.session.get('eye_image')
        state = int(request.POST.get('stateOptions'))
        
        survey = Survey()
        survey.image = EyeImage.objects.get(id=imageId)
        survey.state = state

        # Not manic
        if  state < 2:
            if request.POST.get('otherOptions0'):
                flash = int(request.POST.get('otherOptions0'))
            survey.flash = flash

        # Manic
        else:
            mentalOptions = request.POST.getlist('mentalOptions')
            mental = ','.join(mentalOptions)
            medicationOptions = request.POST.getlist('medicationOptions')
            medication = ','.join(medicationOptions)
            medicationOther = request.POST.get('medicationOther')
            substancesOptions = request.POST.getlist('substancesOptions')
            substances = ','.join(substancesOptions)
   
            if request.POST.get('otherOptions'):
                flash = int(request.POST.get('otherOptions'))        
                  
            survey.feelings = mental
            survey.medications = medication + ',' + medicationOther
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

@login_required
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

    #Crop image
    im = Image.open(request.FILES['file0'])
    
    #Need to rotate image if necessary
    try:
        for orientation in ExifTags.TAGS.keys(): 
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(im._getexif().items())

        if  exif[orientation] == 3 : 
            im=im.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            im=im.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            im=im.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        #traceback.print_exc()
        pass

    # if im.size[0] > im.size[1]:
    #   im = im.transpose(Image.ROTATE_270)
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

    request.session['eye_image'] = eye_image_crop.id

    #encrypt the image
    # password = "theImagePassword$"
    # hasher = SHA256.new(password.encode("latin-1"))
    # digest = hasher.digest()
    # filename = crop_path
    # encrypt(digest, filename)

    #upload to S3
    if 'AWS_ACCESS_KEY_ID' in os.environ:   
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
    else:
        s3 = boto3.client(
            's3'
        )

    filename = crop_path
    bucket_name = 'smu-mania-study-images'
    s3.upload_file(filename, bucket_name, 'images/{}'.format(request.user.username + '_' + ts + '_crop.png'))

    orig_image = settings.MEDIA_ROOT + '/img/' + request.user.username + '_' + ts + '.png'    
    os.remove(filename)
    os.remove(orig_image)
    return render(request, 'collection/survey.html')

@login_required
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
