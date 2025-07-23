from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, PermissionViewSet

group_router = DefaultRouter()
group_router.register(r'', GroupViewSet, basename='group')

permission_router = DefaultRouter()
permission_router.register(r'', PermissionViewSet, basename='permission')
