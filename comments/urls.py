from django.conf.urls import url

from . import views

app_name='comments'

urlpatterns = [
    url(r'^comment/$', views.post_comment, name='post_comment'),
]