from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^client_request/$', views.client_request)
]

# urlpatterns = [
#     url(r'^client_request/$', views.client_request),
# ]
