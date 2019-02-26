from django.conf.urls import url
from django.urls import path
from . import views
from . import consumers

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.WebsocketConsumer),
    # url(r'^client_request/$', views.client_request)
]

# urlpatterns = [
#     url(r'^client_request/$', views.client_request),
# ]
