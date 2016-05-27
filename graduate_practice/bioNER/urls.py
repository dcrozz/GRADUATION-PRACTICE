from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='bioNER'),
	#  url(r'^add/$',views.add,name='add'),
	url(r'^process/$',views.process,name='process'),
        #  url(r'^ajax_list/$', views.ajax_list, name='ajax-list'),
        #  url(r'^ajax_dict/$', views.ajax_dict, name='ajax-dict'),
]
