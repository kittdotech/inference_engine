from django.conf.urls import url
import os
from . import views
from . import view_upload

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate$',views.generate,name="generate"),
    url(r'^list/$', view_upload.list, name='list'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
    ]

