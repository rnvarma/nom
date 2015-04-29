from django.conf.urls import patterns, include, url
from django.contrib import admin
from nom.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomepageView.as_view()),
    url(r'^company/(?P<id>[0-9]+)/$', CompanyView.as_view()),
    url(r'^signup$', SignupView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^login$', LoginView.as_view()),
    url(r'^createevent$', EventCreationView.as_view()),
    url(r'^createorganization', OrganizationCreationView.as_view()),
    url(r'^joinevent/(?P<id>[0-9]+)$', EventJoin.as_view()),
    url(r'^event/(?P<id>[0-9]+)$', EventPageView.as_view())
)