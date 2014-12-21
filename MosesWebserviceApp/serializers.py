from rest_framework import serializers
from MosesWebserviceApp.models import User, Bill, Group, GroupUser
from collections import OrderedDict

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'full_name', 'email', 'facebook_id', 'locale', 'timezone')


class GroupSerializer(serializers.ModelSerializer):

    def __str__(self):
        return "1111"

    class Meta:
        model = Group
        fields = ('id', 'name', 'owner', 'status')


class BillSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'group', 'receiver', 'debtor', 'amount', 'deadline', 'status')


class GroupUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group')



