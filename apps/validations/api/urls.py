"""
Validations API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.validations.api import views

router = routers.DefaultRouter()
router.register(r'qa-validations', views.ValidationView)
router.register(r'wips', views.WorkInProgressView)

app_name = "validations"

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^qa-validations/(?P<id>.+)/signed$',
            views.SignedValidationView.as_view(),
            name='signed_validation_view'),
    re_path(r'^wips/(?P<id>.+)/signed$',
            views.SignedWipView.as_view(),
            name='signed_wip_view'),

]
