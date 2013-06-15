from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pxemngr.views.home', name='home'),
    # url(r'^pxemngr/', include('pxemngr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^localboot/(?P<mac>[a-fA-F0-9:-]+)/$', 'pxe.views.localboot'),
    (r'^localboot/$', 'pxe.views.localboot1'),
    (r'^profile/(?P<mac>[a-fA-F0-9:-]+)/$', 'pxe.views.profile'),
    (r'^profile/$', 'pxe.views.profile1'),
                       
    (r'^upload/(?P<logid>[0-9]+)/$', 'tester.views.upload_file'),
    (r'^nexttest/$', 'tester.views.next_test1'),
    (r'^nexttest/(?P<mac>[a-fA-F0-9:-]+)/$', 'tester.views.next_test'),
    
    (r'^$', 'tester.views.index'),
    (r'^tests/(?P<verid>[0-9]+)/$', 'tester.views.logs'),
    (r'^test/(?P<logid>[0-9]+)/$', 'tester.views.log'),
    (r'^testcontent/(?P<logid>[0-9]+)/$', 'tester.views.content'),
    (r'^script/(?P<name>.+)/$', 'tester.views.script'),
    (r'^system/(?P<sysid>[0-9]+)/$', 'tester.views.system'),
    (r'^testname/(?P<tstid>[0-9]+)/$', 'tester.views.testname'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
