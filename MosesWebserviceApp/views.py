from MosesWebserviceApp.models import User, Group, Bill, BillUser, GroupUser
from MosesWebserviceApp.serializers import UserSerializer, GroupSerializer, BillSerializer,\
    ReadGroupUserSerializerUser, ReadGroupUserSerializerGroup, WriteGroupUserSerializer, BillUserSerializerUser
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from MosesWebservice.settings import SERVER_URL


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        '[CRUD] Users': reverse('user-crud', request=request, format=format),
        '[CRUD] Group': reverse('group-crud', request=request, format=format),
        '[CREATE] Group_User': reverse('group_user-create', request=request, format=format),
        '[READ] User groups': SERVER_URL + 'group_user_user/$id',
        '[READ] Group users': SERVER_URL + 'group_user_group/$id',
        '[CREATE] Bill': SERVER_URL + 'bill/',
        '[CRUD] Bill_User': reverse('bill_user-crud', request=request, format=format),
        '[READ] Bill_User': SERVER_URL + 'bill_user/$id',
    })


# User CRUD
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'facebook_id'
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Group CRUD
class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        instance = serializer.save()
        GroupUser(user=instance.creator, group=instance, administrator=True).save()


# Bill Create
class BillCreate(generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


# BillUser CRUD
class BillUserList(generics.ListCreateAPIView):
    queryset = BillUser.objects.all()
    serializer_class = BillUserSerializerUser
    permission_classes = (permissions.IsAuthenticated,)


class BillUserDetail(generics.ListAPIView):
    serializer_class = BillUserSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return BillUser.objects.filter(member__pk=key)


# GroupUser CRUD
class GroupUserCreate(generics.CreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = WriteGroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserDetailUser(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(user__pk=key)


class GroupUserDetailGroup(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerGroup
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(group__pk=key)