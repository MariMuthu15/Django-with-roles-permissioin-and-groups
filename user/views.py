from django.shortcuts import render
from django.contrib.auth.models import Group, User, Permission, ContentType
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db import transaction
from rest_framework import viewsets

from user.serializers import GroupSerializer, PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = None
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete", "put")


    def list(self, request, *args, **kwargs):
        return super().list(request, fields=("id", "name"), *args, **kwargs)
    

class PermissionViewSet(viewsets.ModelViewSet):

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    pagination_class = None
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "codename"
    http_method_names = ("get", "post")

    

class GroupViewSetWithPermissions(viewsets.ModelViewSet):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = None
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete", "put")

    def list(self, request, *args, **kwargs):
        return super().list(request, fields=("id", "name", "permissions"), *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # Get or create the group
        group, created = Group.objects.get_or_create(name='Interviewers')

        # Get the permissions you want to assign
        content_type = ContentType.objects.get_for_model(request.data.get('model'))
        permission = Permission.objects.get(
            codename=request.data.get('codename'),
            content_type=content_type,
        )

        # Add the permission to the group
        group.permissions.add(permission)
        group.save()
        return Response(
            {"message": f"Permissions have been assigned to group {group.name}."},
            status=status.HTTP_200_OK,
        )



class AssignPermissionsToUser(generics.GenericAPIView):

    serializer_class = GroupSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        username = request.data.get("name", "")
        user = User.objects.filter(username=username).first()
        
        if not user:
            return Response(
                {"error": f"User with username '{username}' does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        with transaction.atomic():
            if user.groups.exists():
                group = user.groups.first()
                serializer = self.get_serializer(group, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                request.data["name"] = user.username
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                group = serializer.save()
                user.groups.add(group)
            
            return Response(
                {"message": f"Permissions have been assigned to {user.username}."},
                status=status.HTTP_200_OK,
            )


    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user.groups.exists():
            serializer = self.get_serializer(user.groups.first())
        else:
            group = Group.objects.create(name=username)
            user.groups.add(group)
            serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserPermissionApi(generics.GenericAPIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.exists():
            serializer = PermissionSerializer(
                request.user.groups.first().permissions,
                fields=("id", "codename"),
                many=True,
            )
        else:
            group = Group.objects.create(name=request.user)
            request.user.groups.add(group)
            serializer = PermissionSerializer(
                group.permissions, fields=("id", "codename"), many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserPermissionWithGroup(generics.GenericAPIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.exists():
            serializer = GroupSerializer(
                request.user.groups.first(),
                fields=("id", "name", "permissions"),
            )
        else:
            group = Group.objects.create(name=request.user)
            request.user.groups.add(group)
            serializer = GroupSerializer(group, fields=("id", "name", "permissions"))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        group_name = request.data.get("group_name")

        if not username or not group_name:
            return Response(
                {"error": "Both 'username' and 'group_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                {"error": f"User '{username}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return Response(
            {"message": f"Group '{group.name}' assigned to user '{user.username}'."},
            status=status.HTTP_200_OK,
        )
