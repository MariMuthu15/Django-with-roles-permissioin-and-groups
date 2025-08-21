from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType


class DynamicModelPermission(permissions.BasePermission):
    """
    Dynamically checks model-level permissions for any ViewSet
    based on the action and queryset.model.
    """

    # Default mapping DRF action -> Django permission type
    default_perm_map = {
        "create": "add",
        "list": "view",
        "retrieve": "view",
        "update": "change",
        "partial_update": "change",
        "destroy": "delete",
    }

    def has_permission(self, request, view):
        # Get the action
        action = getattr(view, "action", None)
        if not action:
            return False

        # Map action to Django codename type
        perm_type = self.default_perm_map.get(action)
        if not perm_type:
            return False

        # Infer model from queryset
        model_cls = getattr(getattr(view, "queryset", None), "model", None)
        if not model_cls:
            return False

        # Build permission codename
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.model_name
        codename = f"{app_label}.{perm_type}_{model_name}"

        # Debug (optional)
        # print("Checking permission:", codename)

        return request.user.has_perm(codename)
