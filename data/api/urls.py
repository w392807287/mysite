from django.conf.urls import url
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^area_housing_prices/$', AreaHousingPriceList.as_view(), name='entity-areas'),
    # url(r'^areas/(?P<pk>[0-9]+)/$', AreatDetail.as_view(), name='areas-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)