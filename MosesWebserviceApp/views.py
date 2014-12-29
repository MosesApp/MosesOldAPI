from MosesWebserviceApp.models import User, Group, Bill, GroupUser
from MosesWebserviceApp.serializers import UserSerializer, GroupSerializer, BillSerializer, GroupUserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q


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


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'facebook_id'
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


class BillDetail(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        key = self.kwargs['pk']
        return Bill.objects.filter(Q(debtor__pk=key) | Q(receiver__pk=key))


class GroupUserList(generics.ListCreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserDetail(generics.ListAPIView):
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        key = self.kwargs['pk']
        return GroupUser.objects.filter(Q(user__pk=key))
