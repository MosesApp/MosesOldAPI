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
        fields = ('id', 'bill', 'amount', 'member', 'relation', 'status')


class BillSerializer(serializers.ModelSerializer):

    members = BillUserSerializer(many=True)

    def create(self, validated_data):
        members_data = validated_data.pop('members')

        # Validate Bill and Members
        taker = False
        debtor = False
        debtors_total = 0.0
        for member in members_data:
            member = list(member.items())
            if len(member) < 4:
                raise serializers.ValidationError("A member is composed of four attributes: "
                                                  "member, relation, status and amount")
            if member and \
               member[0][0] == 'amount' and\
               member[1][0] == 'member' and \
               member[2][0] == 'relation' and \
               member[3][0] == 'status':

                amount = member[0]
                memberObj = member[1]
                relation = member[2]
                status = member[3]

                if relation[1] == 'taker':
                    taker = True
                    if amount[1] or status[1]:
                        raise serializers.ValidationError("Amount, and status must be null for taker")
                elif relation[1] == 'debtor':
                    debtor = True
                    if not amount[1] or not status[1]:
                        raise serializers.ValidationError("Amount, or status cannot be null for debtor")
                    debtors_total = debtors_total + amount[1]
                else:
                    raise serializers.ValidationError("Bill member should be a taker, or a debtor")

                if relation[1] == 'debtor' and (amount[1] <= 0.0 or amount[1] > validated_data['amount']):
                    raise serializers.ValidationError("Bill member should be assigned an amount higher than "
                                                      "zero and lower equal than the total amount")

                if not GroupUser.objects.filter(group=validated_data['group'], user=memberObj[1]).exists():
                    raise serializers.ValidationError("Member %s does not exist in group %s" %
                                                      (memberObj[1], validated_data['group']))

        if not taker or not debtor:
            raise serializers.ValidationError("A bill should be composed from at least one taker, and one debtor")

        if debtors_total != validated_data['amount']:
            raise serializers.ValidationError("Debtors summed amount not equal to Bill amount")

        # Save Bill and Members
        bill = Bill.objects.create(**validated_data)
        bill.members = []
        for member in members_data:
            member = list(member.items())
            if member and \
                member[0][0] == 'amount' and \
                member[1][0] == 'member' and \
                member[2][0] == 'relation' and \
                member[3][0] == 'status':

                amount = member[0]
                memberObj = member[1]
                relation = member[2]
                status = member[3]

                bill.members.append(BillUser.objects.create(bill=bill,
                                                            amount=amount[1],
                                                            member=memberObj[1],
                                                            relation=relation[1],
                                                            status=status[1]))

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



