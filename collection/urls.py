from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^index/$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^complete/$', views.complete, name='complete'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^consent/$', views.consent, name='consent'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^profile/$', views.profile, name='profile')
]