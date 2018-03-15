from django.conf.urls import url
from django.conf import settings
from notification_channels.views import *


app_name='notifications'



urlpatterns = [
		
	url(r'^$', notifications, name='notifications'),
	url(r'^/read-all/$', read_all, name='read_all'),

]