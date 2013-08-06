from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from tracking.views import tracking
admin.autodiscover()

urlpatterns = patterns('tracking.views',

    #url(r'^contact/(?P<pk>\d+)/$', 'detail'),
    (r'^edit_con/(\d+)/$','edit_con'),
    (r'^edit_driver/(\d+)/$','edit_driver'),
    (r'^edit_installer/(\d+)/$','edit_installer'),
    (r'^search/$','search'),
    (r'^edit_work_order/(\d+)/$','edit_work_order'),
    (r'^new_work_order/$','new_work_order'),
    (r'^new_driver/$','new_driver'),
    (r'^new_contractor/$','new_contractor'),
    (r'^new_installer/$','new_installer'),
    (r'^projects/$','new_project'),
    (r'$','tracking'),
    

   
     

)