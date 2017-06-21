# Mania, A django based app used to collect eye images. 


## How to run the app

1. Create a python virutal environement using conda or virtualenv
2. <code>pip install django-debug-toolbar </code>(a handful debug tool for django)
3. <code>pip install django-registration-redux</code> (used for authentication, the reason why it requires login is because it is easier for
the same user to upload multiple photoes, but it should be easy to change)
4. <code>python manager.py runserver </code> , If you have to create DB first, run the following:  <br />
   <code>python manage.py makemigrations </code>  <br />
   <code>python manage.py migrate </code>

## Other useful info

This app use cropperjs which is a mobile friendly image crop tool <https://github.com/fengyuanchen/cropperjs>
