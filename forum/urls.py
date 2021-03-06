from django.conf.urls import url
from django.views.generic.base import TemplateView


from . import views

# app_name = 'forum'
urlpatterns = [
    url(r'^$', views.Home.as_view(template_name='home.html'), name='home'),
    url(r'^new$', views.PostCreate.as_view(), name='post_create'),
    url(r'^view/(?P<pk>\d+)$', views.PostView.as_view(), name='post_view'),
    url(r'^edit/(?P<pk>\d+)$', views.PostUpdate.as_view(), name='post_update'),
    url(r'^delete/(?P<pk>\d+)$', views.PostDelete.as_view(), name='post_delete'),
    url(r'^(?P<pk>\d+)/comment/$', views.CommentCreate.as_view(), name='comment_create'),
    url(r'^categories/$', views.search_tag, name='search'),
]