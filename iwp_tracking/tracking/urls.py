from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from tracking.views import tracking
admin.autodiscover()

urlpatterns = patterns('tracking.views',

    # url(r'^$', 'tracking.views.main_page'),
    # url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    # (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    # (r'^reset/([0-9A-Za-z]+)-(.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    # (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # url(r'^logout/$', 'tracking.views.logout_page'),
    (r'^search/$','search'),
    (r'^edit_work_order/(\d+)/$','edit_work_order'),
    (r'^new_work_order/$','new_work_order'),
    (r'^new_driver/$','new_driver'),
    (r'^new_contractor/$','new_contractor'),
    (r'^new_installer/$','new_installer'),
    (r'^projects/$','new_project'),
    (r'$','tracking'),
    #(r'^new_work_order$','new_work_order'),
    #url(r'^accounts/', include('invitation.urls')),
    #url(r'^schedule/', include('schedule.urls')),
    #url(r'^project_admin/', include('project_admin.urls')),
    #url(r'^profile/', include('userprofile.urls')),
	#url(r'^resources/', include('resources.urls')),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #    'document_root': settings.MEDIA_ROOT}),
	#(r'$',tracking),

   
     

)