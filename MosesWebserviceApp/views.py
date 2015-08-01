from MosesWebserviceApp.models import User, Group, Bill, UserExpense, GroupUser, Currency
from MosesWebserviceApp.serializers import UserSerializer, GroupSerializer, BillSerializer,\
    ReadGroupUserSerializerUser, ReadGroupUserSerializerGroup, WriteGroupUserSerializer, UserExpenseSerializerUser, \
    CreateGroupSerializer, CurrencySerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict


@api_view(('GET',))
def api_root(request, format=None):

    return Response(OrderedDict([
        ("User", "------------------------------------------------------------------------------"),
        ('[READ ALL] Users', reverse('user-list', request=request, format=format)),
        ('[READ] User (provide facebook_id)', reverse('user-details-filter-facebookid', request=request, args=[1111111111])),
        ('[CREATE] User', reverse('user-create', request=request, format=format)),
        ("Group", "------------------------------------------------------------------------------"),
        ('[READ ALL] Groups', reverse('group-list', request=request, format=format)),
        ('[CREATE] Group', reverse('group-create', request=request, format=format)),
        ("Group_User", "------------------------------------------------------------------------------"),
        ('[READ] Group User Relation (provide group_id)', reverse('group_user-details-filter-groupid', request=request, args=[1111111111])),
        ('[READ] Group User Relation (provide user_id)', reverse('group_user-details-filter-userid', request=request, args=[1111111111])),
        ('[CREATE] Group User Relation', reverse('group_user-create', request=request, format=format)),
        ("Bill", "------------------------------------------------------------------------------"),
        ('[CREATE] Bills', reverse('bill-create', request=request, format=format)),
        ("Bill_User", "------------------------------------------------------------------------------"),
        ('[READ ALL] Bill_Users', reverse('bill_user-list', request=request, format=format)),
        ('[READ] Bill_User Relation (provide user_id)', reverse('bill_user-details', request=request, args=[1111111111])),
        ('[CREATE] Bill_User Relation', reverse('bill_user-create', request=request, format=format)),
        ("Currency", "------------------------------------------------------------------------------"),
        ('[READ ALL] Currencies', reverse('currency-list', request=request, format=format)),
        ('[CREATE] Currency', reverse('currency-create', request=request, format=format))
    ]))


# List all Users
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

# Create a User
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

# List the details from an specific User (filter by facebook_id)
class UserDetails(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        facebook_id_list = self.kwargs['pk'].split("&")
        user_list = User.objects.filter(facebook_id__in=facebook_id_list)
        return user_list


# Create a Group
class GroupCreate(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


# List all Groups
class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Create Group_User
class GroupUserCreate(generics.CreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = WriteGroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# List all Group_User by User_id
class GroupUserDetailUser(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(user__pk=key)


# List all Group_User by Group_id
class GroupUserDetailGroup(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerGroup
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(group__pk=key)


# Create Bill
class BillCreate(generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


# List all Bill_User
class UserExpenseList(generics.ListAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UserExpenseSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

# Create Bill_User
class UserExpenseCreate(generics.CreateAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UserExpenseSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

# List the details from an specific Bill_User (filter by user_id)
class UserExpenseDetail(generics.ListAPIView):
    serializer_class = UserExpenseSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return UserExpense.objects.filter(member__pk=key)


# List all Currency
class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated,)


# Create Currency
class CurrencyCreate(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()
