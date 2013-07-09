from django.conf.urls import patterns, url

from websearch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^likeit/$', views.likeit, name='likeit'),
    url(r'^unlikeit/$', views.unlikeit, name='unlikeit'),
    url(r'^like/$', views.like, name='like'),
    url(r'^checku/$', views.checkuser, name='checku'),
    url(r'^checke/$', views.checkemail, name='checke'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^addmsg/$', views.msg_add, name='addmsg'),
    url(r'^msg/$', views.msg_show, name='showmsg'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^search/$', views.search, name='search'),
)
