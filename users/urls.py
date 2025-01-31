from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from users.views import *

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
    path('generate-username/', GenerateUsernameSlugAPIView.as_view(), name='generate-username'),

    path('assign-bookspace-owner/', AssignBookspaceOwnerView.as_view(), name='assign-bookspace-owner'),
    path('assign-bookspace-manager/', AssignBookspaceManagerView.as_view(), name='assign-bookspace-manager'),
    path('assign-assistant-bookspace-manager/', AssignAssistantBookspaceManagerView.as_view(), name='assign-assistant-bookspace-manager'),
    path('assign-bookspace-worker/', AssignBookspaceWorkerView.as_view(), name='assign-bookspace-worker'),

    path('dismiss-bookspace-manager/', DismissBookspaceManagerView.as_view(), name='dismiss-bookspace-manager'),
    path('dismiss-assistant-bookspace-manager/', DismissAssistantBookspaceManagerView.as_view(), name='dismiss-assistant-bookspace-manager'),
    path('dismiss-bookspace-worker/', DismissBookspaceWorkerView.as_view(), name='dismiss-bookspace-worker'),

    path('', include(router.urls))
]
