from django.conf.urls import patterns, url
from testshare import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^aboutus/$', views.aboutus, name='aboutus'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login,name='login'),
        url(r'^logout/$', views.user_logout,name='logout'),
		url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^updateinfo/$', views.updateinfo, name='updateinfo'),
        url(r'^spread/(?P<post_id>[0-9]+)/$', views.spread, name='spread'),
        ]
