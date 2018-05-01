from django.conf.urls import url, include
from rest_framework import routers

from url_shortener import views


router = routers.DefaultRouter()
router.register(r'shorturls', views.ShortURLViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
