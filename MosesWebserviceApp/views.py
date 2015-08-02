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
        ('[CRUD] Users', reverse('usersCRUD', request=request, format=format)),
        ('[READ] Users from Group {group_id}', reverse('usersByGroup', request=request, args=[1])),
        ('[READ] User {facebook_id}', reverse('userByFacebookId', request=request, args=[1111111111])),
        ("Group", "------------------------------------------------------------------------------"),
        ('[CRUD] Groups', reverse('groupsCRUD', request=request, format=format)),
        ('[CREATE] Add User to Group', reverse('addGroupUser', request=request, format=format)),
        ('[READ] Groups from User {user_id}', reverse('groupsByUser', request=request, args=[1])),
        ("Bill", "------------------------------------------------------------------------------"),
        ('[CREATE] Bills', reverse('billCreate', request=request, format=format)),
        ("Expenses", "------------------------------------------------------------------------------"),
        ('[CRUD] Expenses', reverse('expensesCRUD', request=request, format=format)),
        ('[READ] Expenses by User {user_id}', reverse('expensesByUser', request=request, args=[1])),
        ("Currency", "------------------------------------------------------------------------------"),
        ('[READ ALL] Currencies', reverse('currenciesCRUD', request=request, format=format)),
    ]))


# Users
class UsersCRUD(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# List the details from an specific User (filter by facebook_id)
class UserDetails(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        facebook_id_list = self.kwargs['pk'].split("&")
        user_list = User.objects.filter(facebook_id__in=facebook_id_list)
        return user_list


# Groups
class GroupsCRUD(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Add User to Group
class GroupUserCreate(generics.CreateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = WriteGroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# List all Group_User by User_id
class GroupUserDetailByUser(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(user__pk=key)


# List all Group_User by Group_id
class GroupUserDetailByGroup(generics.ListAPIView):
    serializer_class = ReadGroupUserSerializerGroup
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return GroupUser.objects.filter(group__pk=key)


# Bills
class BillCreate(generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


# Exepenses
class ExpensesCRUD(generics.ListCreateAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UserExpenseSerializerUser
    permission_classes = (permissions.IsAuthenticated,)


# List the details from an specific Bill_User (filter by user_id)
class ExpensesByUser(generics.ListAPIView):
    serializer_class = UserExpenseSerializerUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        key = self.kwargs['pk']
        return UserExpense.objects.filter(member__pk=key)


# Currencies
class CurrenciesCRUD(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated,)
