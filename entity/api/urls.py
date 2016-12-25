from django.conf.urls import url, include
from .views import AreaList


urlpatterns = [
    url(r'areas/$', AreaList.as_view(), name='entity_areas')
]