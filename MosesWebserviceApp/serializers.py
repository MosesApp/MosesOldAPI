from MosesWebserviceApp.models import User, Bill, BillUser, Group, GroupUser, Currency
from rest_framework import serializers
from MosesWebserviceApp.fields import Base64ImageField


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'full_name', 'email', 'facebook_id', 'locale', 'timezone')


class GroupUserSerializer(serializers.ModelSerializer):

    user_facebook = serializers.CharField(max_length=20)

    class Meta:
        model = GroupUser
        fields = ('id', 'user_facebook', 'administrator')


class CreateGroupSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required=False, allow_null=True)
    members = GroupUserSerializer(many=True)

    def create(self, validated_data):
        members_data = validated_data.pop('members')

        # Check for one valid member in the members list
        one_valid_member = False
        for member in members_data:
            member = list(member.items())
            user_facebook = member[0][1]
            user_obj = User.objects.filter(facebook_id=user_facebook)
            if user_obj and validated_data['creator'].facebook_id != user_facebook:
                one_valid_member = True
                break

        if not one_valid_member:
            raise serializers.ValidationError("A group must contain at least one valid member besides it's creator")

        # Save Group and Members
        group = Group.objects.create(**validated_data)
        GroupUser.objects.create(user=validated_data['creator'], group=group, administrator=True)
        group.members = []

        for member in members_data:
            member = list(member.items())
            if len(member) >= 1:
                user_facebook = member[0][1]
                if len(member) == 1:
                    administrator = False
                else:
                    administrator = member[1][1]
                user_obj = User.objects.filter(facebook_id=user_facebook)
                if user_obj:
                    group_user = GroupUser(user=user_obj[0], group=group, administrator=administrator)
                    group_user.user_facebook = user_facebook
                    group_user.save()
                    group.members.append(group_user)

        if len(group.members) == 0:
            raise serializers.ValidationError("Check the group members facebook_id for invalid ones")

        return group

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'creator', 'members')


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
        takers_total = 0.0
        member_obj = None
        bill_users = []

        for member in members_data:
            member = list(member.items())
            # Taker rules
            if len(member) == 3:
                if member[0][0] == 'amount' and\
                   member[1][0] == 'member' and \
                   member[2][0] == 'relation':

                    amount = member[0]
                    member_obj = member[1]
                    relation = member[2]

                    if relation[1] == 'taker':
                        if amount[1] <= 0.0 or amount[1] > validated_data['amount']:
                            raise serializers.ValidationError("Bill member %s should be assigned an amount higher than "
                                                              "zero, and lower equal the bill's total amount" %
                                                              member_obj[1])
                        taker_list.append(member)
                        takers_total = takers_total + amount[1]
                        bill_users.append(BillUser(bill=None,
                                                   amount=amount[1],
                                                   member=member_obj[1],
                                                   relation=relation[1],
                                                   status="not paid"))
                    else:
                        raise serializers.ValidationError("A member is composed of three attributes: "
                                                          "member, relation and amount (if relation=='taker')")
            # Debtor rules
            elif len(member) == 2:

                if member[0][0] == 'member' and \
                   member[1][0] == 'relation':

                    member_obj = member[0]
                    relation = member[1]

                    if relation[1] == 'debtor':
                        debtor_list.append(member)
                        bill_users.append(BillUser(bill=None,
                                                   amount=0.0,
                                                   member=member_obj[1],
                                                   relation=relation[1],
                                                   status="not paid"))
                    else:
                        raise serializers.ValidationError("A member is composed of three attributes: "
                                                          "member, relation and amount (if relation=='taker')")
            else:
                raise serializers.ValidationError("A member is composed of three attributes: "
                                                  "member, relation and amount (if relation=='taker')")

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
            raise serializers.ValidationError("Takers summed amount must be equal to bill amount")

        debtor_val = float(validated_data['amount']) / (len(taker_list) + len(debtor_list))

        # Save Bill and Members
        bill = Bill.objects.create(**validated_data)
        bill.members = []

        for bill_user in bill_users:
            bill_user.bill = bill
            if bill_user.relation == "debtor":
                bill_user.amount = debtor_val
            elif bill_user.relation == "taker":
                bill_user.amount -= debtor_val
            bill_user.save()
            bill.members.append(bill_user)

        return bill

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'currency', 'date', 'members')


class BillSerializerStandard(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'currency', 'date')


class BillUserSerializerUser(serializers.ModelSerializer):

    bill = BillSerializerStandard()

    class Meta:
        model = BillUser
        fields = ('id', 'bill', 'amount', 'member', 'relation', 'status')


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


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'prefix', 'description')



