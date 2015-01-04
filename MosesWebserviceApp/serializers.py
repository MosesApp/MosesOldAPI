from rest_framework import serializers
from MosesWebserviceApp.models import User, Bill, Group, GroupUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'full_name', 'email', 'facebook_id', 'locale', 'timezone')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'owner', 'status')


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'group', 'receipt_image', 'receiver', 'debtor', 'amount', 'deadline', 'status')


class BillReceiverSerializer(serializers.ModelSerializer):

    debtor = UserSerializer()

    class Meta:
        model = Bill
        fields = ('id', 'group', 'receipt_image', 'receiver', 'debtor', 'amount', 'deadline', 'status')


class BillDebtorSerializer(serializers.ModelSerializer):

    receiver = UserSerializer()

    class Meta:
        model = Bill
        fields = ('id', 'group', 'receipt_image', 'receiver', 'debtor', 'amount', 'deadline', 'status')


class GroupUserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group')


class WriteGroupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group')



