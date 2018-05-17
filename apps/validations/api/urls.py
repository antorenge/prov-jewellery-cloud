"""
Validations API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.validations.api import views

router = routers.DefaultRouter()
router.register(r'validations', views.ValidationView)
router.register(r'wips', views.WorkInProgressView)

app_name = "validations"

urlpatterns = [
    re_path(r'^', include(router.urls)),

]
