from django.contrib import admin
from .models import EyeImage, Survey, Profile

# Register your models here.
admin.site.register(EyeImage)
admin.site.register(Survey)
admin.site.register(Profile)