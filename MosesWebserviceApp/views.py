from MosesWebserviceApp.models import User, Group, Bill, GroupUser
from MosesWebserviceApp.serializers import UserSerializer, GroupSerializer, BillSerializer, \
    BillDebtorSerializer, BillReceiverSerializer, GroupUserSerializer, WriteGroupUserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'List all Users': reverse('user-list', request=request, format=format),
        'List all Bills': reverse('bill-list', request=request, format=format),
        'List all Groups': reverse('group-list', request=request, format=format),
        'Create Group_User relation': reverse('group_user-create', request=request, format=format),
        'List all Group_Users': reverse('group_user-list', request=request, format=format)
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


class BillDetailReceiver(generics.ListAPIView):
    serializer_class = BillReceiverSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return Bill.objects.filter(Q(receiver__pk=key))


class BillDetailDebtor(generics.ListAPIView):
    serializer_class = BillDebtorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return Bill.objects.filter(Q(debtor__pk=key))


class GroupUserList(generics.ListAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserCreate(generics.CreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = WriteGroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupUserDetail(generics.ListAPIView):
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(Q(user__pk=key))
