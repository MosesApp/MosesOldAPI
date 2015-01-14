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
        fields = ('id', 'bill', 'amount', 'member', 'relation')


class BillSerializer(serializers.ModelSerializer):

    members = BillUserSerializer(many=True)

    def create(self, validated_data):
        members_data = validated_data.pop('members')

        # Validate Bill and Members
        debtor_list = []
        taker_list = []
        debtors_total = 0.0
        takers_total = 0.0

        for member in members_data:
            member = list(member.items())
            if len(member) < 3:
                raise serializers.ValidationError("A member is composed of four attributes: "
                                                  "member, relation, status and amount")
            if member and \
               member[0][0] == 'amount' and\
               member[1][0] == 'member' and \
               member[2][0] == 'relation':

                amount = member[0]
                member_obj = member[1]
                relation = member[2]

                if relation[1] == 'taker':
                    taker_list.append(member)
                    takers_total = takers_total + amount[1]
                elif relation[1] == 'debtor':
                    debtor_list.append(member)
                    debtors_total = debtors_total + amount[1]
                else:
                    raise serializers.ValidationError("Bill member should be a taker, or a debtor")

                if amount[1] <= 0.0 or amount[1] > validated_data['amount']:
                    raise serializers.ValidationError("Bill member %s should be assigned an amount higher than "
                                                      "zero and lower equal the bill's total amount" % member[1][1])

                if not GroupUser.objects.filter(group=validated_data['group'], user=member_obj[1]).exists():
                    raise serializers.ValidationError("Member %s is not in group %s" %
                                                      (member_obj[1], validated_data['group']))

        for debtor_i in debtor_list:
            for taker_i in taker_list:
                if taker_i[1][1] == debtor_i[1][1]:
                    raise serializers.ValidationError("Member %s cannot be a debtor and taker at the same time"
                                                      % taker_i[1][1])

        if not taker_list or not debtor_list:
            raise serializers.ValidationError("Bill should be composed from at least one taker, and one debtor")

        if takers_total != validated_data['amount']:
            raise serializers.ValidationError("Takers summed amount must be equal bill value")

        if debtors_total >= validated_data['amount']:
            raise serializers.ValidationError("Debtors summed amount must be lower than bill amount")

        # Save Bill and Members
        bill = Bill.objects.create(**validated_data)
        bill.members = []
        for member in members_data:
            member = list(member.items())
            if member and \
                member[0][0] == 'amount' and \
                member[1][0] == 'member' and \
                member[2][0] == 'relation':

                amount = member[0]
                member_obj = member[1]
                relation = member[2]
                status = "not paid"

                bill.members.append(BillUser.objects.create(bill=bill,
                                                            amount=amount[1],
                                                            member=member_obj[1],
                                                            relation=relation[1],
                                                            status=status))

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



