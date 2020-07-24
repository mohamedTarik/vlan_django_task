
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('vlandata',views.Vlans_APIS,basename='vlandata')



urlpatterns = [
    path('', include(router.urls)),

]
