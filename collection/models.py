from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

# Create your models here.
class EyeImage(models.Model):
	participant = models.ForeignKey(User, on_delete=models.CASCADE)
	image_id = models.IntegerField()
	eye_image = models.ImageField(upload_to = 'img/')
	dateTime = models.DateTimeField(auto_now_add=True)
	image_name = models.CharField(max_length=200, default='')
	def __str__(self):
   		return self.image_name

class Survey(models.Model):
	image = models.ForeignKey(EyeImage, on_delete=models.CASCADE)
	feelings = models.IntegerField()
	state = models.IntegerField()
	medications = models.CharField(max_length=200)
	substances = models.IntegerField()
	flash = models.IntegerField()

	def __str__(self):
		return 'Survey of image ' + self.image.image_name

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	age = models.IntegerField()
	gender = models.IntegerField()
	diagnosis = models.IntegerField()

	def __str__(self):
		return 'Profile of user ' + self.user.username