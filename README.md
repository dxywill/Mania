# Mania, A django based app used to collect eye images. 


## How to run the app in your local environemnt 

1. Create a python virutal environement using conda or virtualenv
2. Activate virtual environment using:
   * source yourvirtualenvfolder/bin/activate  (using virtualenv)
   * source activate yourvirtualenvname (using anaconda) 
3. <code>pip install django==1.10.5 (the latest version (1.11.0 or later ) may cause some issues) </code>
4. <code>pip install django-debug-toolbar </code>(a handful debug tool for django)
5. <code>pip install django-registration-redux</code> (used for authentication, the reason why it requires login is because it is easier for
the same user to upload multiple photoes, but it should be easy to change)
6. <code>pip install pillow (for image processing) </code>
7. <code>pip install pycryptodome (for image encryption) </code>
8. <code>pip install mysqlclient (for mysql db access) </code>
9. <code>python manager.py runserver </code> , If you have to create DB first, run the following:  <br />
   <code>python manage.py makemigrations </code>  <br />
   <code>python manage.py migrate </code>


## Deploy to Apache + mod_wsgi + Linux (Ubuntu 16.04)

0. Create a MySql database in your localhost called maniahero
1. Create a virtual host in /etc/apache2/sites-available/ (you can just drop in the mania.conf, this config file assumes you put your website under /var/www/Mania/, if you use a different location, you may need to change the config file accordingly)
2. enable the site by running <code> a2ensite mania </code>
3. restart apache server by running <code> sudo service apache2 restart </code>

## Other useful info

This app use cropperjs which is a mobile friendly image crop tool <https://github.com/fengyuanchen/cropperjs>
