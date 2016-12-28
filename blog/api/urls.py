from django.conf.urls import url
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts$', UserPostList.as_view(), name='userpost-list'),
    url(r'^authors/(?P<username>[0-9a-zA-Z_-]+)$', AuthorDetail.as_view(), name='user-detail'),
    url(r'^authors/$', AuthorList.as_view(), name='user-list')
]

urlpatterns = format_suffix_patterns(urlpatterns)