from MosesWebserviceApp.models import User, Group, Bill, GroupUser
from MosesWebserviceApp.serializers import UserSerializer, GroupSerializer, BillSerializer, GroupUserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'bills': reverse('bill-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'group_users': reverse('group_user-list', request=request, format=format)
    })


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BillList(generics.ListCreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BillDetail(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserList(generics.ListCreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserDetail(generics.RetrieveAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
