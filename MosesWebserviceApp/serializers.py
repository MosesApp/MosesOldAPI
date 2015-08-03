from MosesWebserviceApp.models import User, Bill, Expense, Group, GroupUser, Currency
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
            user = User.objects.filter(facebook_id=member['user_facebook'])
            if user and validated_data['creator'].facebook_id != member['user_facebook']:
                one_valid_member = True
                break

        if not one_valid_member:
            raise serializers.ValidationError("A group must contain at least one valid member besides it's creator")

        # Save Group and Members
        group = Group.objects.create(**validated_data)
        GroupUser.objects.create(user=validated_data['creator'], group=group, administrator=True)
        group.members = []

        for member in members_data:
            if 'administrator' not in member:
                member['administrator'] = False

            user = User.objects.filter(facebook_id=member['user_facebook'])
            if not user or 'user_facebook' not in member:
                raise serializers.ValidationError("Check the group members facebook_id for invalid ones")

            group_user = GroupUser(user=user[0], group=group, administrator=member['administrator'])
            group_user.user_facebook = member['user_facebook']
            group_user.save()
            group.members.append(group_user)
        return group

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'creator', 'members')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'image', 'creator', 'status')


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ('id', 'bill', 'amount', 'user', 'relation')


class BillSerializer(serializers.ModelSerializer):

    receipt_image = Base64ImageField(required=False, allow_null=True)
    expenses = ExpenseSerializer(many=True)

    def create(self, validated_data):
        expenses_data = validated_data.pop('expenses')

        # Validate Bill and Members
        debtor_list = []
        taker_list = []
        takers_total = 0.0
        member = None
        expenses = []

        for expense in expenses_data:
            # Taker rules
            if 'relation' not in expense:
                raise serializers.ValidationError("All expenses must have a relation ('taker' or 'debtor')")

            if 'user' not in expense:
                raise serializers.ValidationError("All expenses must have an user")

            if not GroupUser.objects.filter(group=validated_data['group'], user=expense['user']).exists():
                raise serializers.ValidationError("User %s is not in group %s" %
                                                  (expense['user'].full_name, validated_data['group']))

            if expense['relation'] is 'taker':
                if 'amount' not in expense or expense['amount'] <= 0.0 or expense['amount'] > validated_data['amount']:
                    raise serializers.ValidationError("Expense %s should be assigned"
                    "an amount higher than zero, and lower equal the bill's total amount" %
                    expense['user'].full_name)

                taker_list.append(expense)
                takers_total = takers_total + expense['amount']
                expenses.append(Expense(bill=None,
                                           amount=expense['amount'],
                                           user=expense['user'],
                                           relation=expense['relation'],
                                           status="not paid"))


            elif expense['relation'] is 'debtor':
                    debtor_list.append(expense)
                    expenses.append(Expense(bill=None,
                                               amount=0.0,
                                               user=expense['user'],
                                               relation=expense['relation'],
                                               status="not paid"))
            else:
                raise serializers.ValidationError("The expense has an invalid relation")

        for debtor in debtor_list:
            for taker in taker_list:
                if taker['user'] == debtor['user']:
                    raise serializers.ValidationError("Expense %s cannot be a debtor and taker at the same time"
                                                      % taker['user'].full_name)

        if not taker_list or not debtor_list:
            raise serializers.ValidationError("Bill should be composed from at least one taker, and one debtor")

        if takers_total != validated_data['amount']:
            raise serializers.ValidationError("Takers summed amount must be equal to bill amount")

        debtor_val = float(validated_data['amount']) / (len(taker_list) + len(debtor_list))

        # Save Bill and Members
        bill = Bill.objects.create(**validated_data)
        bill.expenses = []

        for expense in expenses:
            expense.bill = bill
            if expense.relation == "debtor":
                expense.amount = debtor_val
            elif expense.relation == "taker":
                expense.amount -= debtor_val
            expense.save()
            bill.expenses.append(expense)

        return bill

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'currency', 'date', 'expenses')


class BillSerializerStandard(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'group', 'receipt_image', 'amount', 'currency', 'date')


class ExpenseByUserSerializer(serializers.ModelSerializer):

    bill = BillSerializerStandard()

    class Meta:
        model = Expense
        fields = ('id', 'bill', 'amount', 'user', 'relation', 'status')


class GroupUserByUserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')


class GroupUserByGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')


class AddGroupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupUser
        fields = ('id', 'user', 'group', 'administrator')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'prefix', 'description')
