from rest_framework import serializers
from MosesWebserviceApp.models import User, Bill, Group, GroupUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'full_name', 'email', 'facebook_id', 'locale', 'timezone')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'owner', 'status')


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'group', 'receiver', 'debtor', 'amount', 'deadline', 'status')


class GroupUserSerializer(serializers.ModelSerializer):

    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group')



