from rest_framework import serializers
from MosesWebserviceApp.models import User, Bill, BillUser, Group, GroupUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'full_name', 'email', 'facebook_id', 'locale', 'timezone')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'creator', 'status')


class BillUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillUser
        fields = ('id', 'bill', 'member', 'relation', 'status')


class BillSerializer(serializers.ModelSerializer):

    members = BillUserSerializer(many=True)

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        bill = Bill.objects.create(**validated_data)
        bill.members = []
        for member in members_data:
            member = list(member.items())
            if member and \
               member[0][0] == 'member' and \
               member[1][0] == 'relation' and \
               member[2][0] == 'status':
                bill.members.append(BillUser.objects.create(bill=bill,
                                                            member=member[0][1],
                                                            relation=member[1][1],
                                                            status=member[2][1]))

        return bill

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'deadline', 'members')


class BillSerializerStandard(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'deadline')


class BillUserSerializerUser(serializers.ModelSerializer):

    bill = BillSerializerStandard()

    class Meta:
        model = BillUser
        fields = ('id', 'bill', 'member', 'relation', 'status')


class ReadGroupUserSerializerUser(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')


class ReadGroupUserSerializerGroup(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')


class WriteGroupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')



