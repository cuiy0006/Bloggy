from django.conf.urls import url
from users import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    #Form where the user submit the email address
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #Page displayed to user after submitting the email form
    url(r'^password_reser_done/$', auth_views.password_reset_done, name='password_reset_done'),
    #The link that was sent to the user
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_complete'),
    #Page displayed to the user after the password was successfully changed
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]