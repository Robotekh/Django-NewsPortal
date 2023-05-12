from rest_framework import routers
from . import views
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'schools', views.SchoolViewset)
router.register(r'classes', views.SClassViewset)
router.register(r'students', views.StudentViewest)


urlpatterns = [
   path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]