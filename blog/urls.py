from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html/$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^full-width-index.html/$', views.fullWidthIndex, name='fullWidthIndex'),
    url(r'^full-width-post/(?P<pk>[0-9]+)/$', views.fullWidthDetial, name='fullWidthDetial'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archive, name="archive"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category')
]