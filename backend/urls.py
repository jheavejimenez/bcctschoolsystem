from django.conf.urls import url

from backend.views import about_view, contact_view, index, login_view, registration_view, oldstud_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^contact-us$', contact_view, name='contact-us'),
    url(r'^about-us$', about_view, name='about-us'),
    url(r'^login$', login_view, name='login'),
    url(r'^registration$', registration_view, name='registration'),
    url(r'^oldstud$', oldstud_view, name='oldstud'),

]
