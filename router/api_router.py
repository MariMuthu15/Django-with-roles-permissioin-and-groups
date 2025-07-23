from django.urls import path, include
from user.urls import group_router, permission_router
from user.views import AssignPermissionsToUser as AssignPermissions, UserPermissionApi, UserPermissionWithGroup



urlpatterns = [
    path('group/', include(group_router.urls )),
    path('permission/', include(permission_router.urls)),
    path('assign-permissions/', AssignPermissions.as_view(), name='assign-permissions'),
    path('user-permissions/', UserPermissionApi.as_view(), name='user-permissions'),
    path('user-permissions-with-group/', UserPermissionWithGroup.as_view(), name='user-permissions-with-group'),
]
