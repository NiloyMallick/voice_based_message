from django.conf.urls import url, include
from . import views

app_name = 'homepage'

urlpatterns = [
    url(r'^$', views.login_view, name="login"),
    url(r'^compose/$', views.group_create_view, name="compose"),
    url(r'^inbox/$', views.get_message, name="inbox"),
    url(r'^sent/$', views.sent_view, name="sent"),
    url(r'^all/$', views.all_message_view, name="all_message"),
    url(r'^options/$', views.options_view, name="options"),
    # url(r'^group/$', views.group_create_view, name="group"),
    url(r'^message/$', views.get_message, name="get_message"),
   
]
