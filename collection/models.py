from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EyeImage(models.Model):
	participant = models.ForeignKey(User, on_delete=models.CASCADE)
	image_id = models.IntegerField()
	eye_image = models.ImageField(upload_to = 'img/')