from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/$', include(admin.site.urls)),
    url(r'^$', 'school.stjoseph.views.home'),
    url(r'^register/$', 'school.stjoseph.views.register'),
    url(r'^activate/(\w+)/$', 'school.stjoseph.views.activate'),
    url(r'^login/$', 'school.stjoseph.views.loginu'),
    url(r'^logout/$', 'school.stjoseph.views.logoutu'),
    url(r'^contact/$', 'school.stjoseph.views.contact'),
    url(r'^gallery/snaps/(?P<path>.*)$', 'school.stjoseph.views.showimage'),
    url(r'^gallery/(\d+)/$', 'school.stjoseph.views.gallery'),
    url(r'^gallery/$', 'school.stjoseph.views.gallery'),
    url(r'^alumni/$', 'school.stjoseph.views.alumni'),
    url(r'^students/$', 'school.stjoseph.views.students'),
    url(r'^staff/$', 'school.stjoseph.views.staff'),
    url(r'^history/$', 'school.stjoseph.views.history'),
    url(r'^song/$', 'school.stjoseph.views.song'),
    url(r'^principal/$', 'school.stjoseph.views.principal'),
    url(r'^information/$', 'school.stjoseph.views.information'),
    url(r'^activities/$', 'school.stjoseph.views.activities'),
    url(r'^infrastructure/$', 'school.stjoseph.views.infrastructure'),
    url(r'^halloffame/$', 'school.stjoseph.views.halloffame'),
    url(r'^profile/(\d+)/$', 'school.stjoseph.views.profile'),
    url(r'^edit/$', 'school.stjoseph.views.edit'),
    url(r'^changepass/$', 'school.stjoseph.views.changepass'),
    url(r'^forgotpass/$', 'school.stjoseph.views.forgotpass'),
    url(r'^newpass/(\d+)/(\w+)/$', 'school.stjoseph.views.newpass'),
    #url(r'^uploadimage/$', 'school.stjoseph.views.uploadimage'),
    #url(r'^printdata/$', 'school.stjoseph.views.printdata'),
)

handler404 = 'stjoseph.views.handle_404'
handler500 = 'stjoseph.views.handle_500'

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/thumb/(?P<path>.*)$', 'school.stjoseph.views.servethumb'),
    url(r'^media/snaps/(?P<path>.*)$', 'school.stjoseph.views.servephoto'),
)
