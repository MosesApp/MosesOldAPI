import uuid
from django.db import models
from MosesWebservice.settings import GROUP_STATUS, PAYMENT_STATUS, PAYMENT_CURRENCY, MEDIA_ROOT, BILL_RELATION
import os


def get_unique_image_file_path(instance=None, filename='dummy.jpg'):
    """
    function to determine where to save images.  assigns a uuid (random string) to each and places it
    in the images subdirectory below media.  by default, we assume the file is a .jpg
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return MEDIA_ROOT + filename


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    full_name = models.CharField(max_length=300, blank=False)
    email = models.CharField(max_length=254, blank=False, unique=True)
    facebook_id = models.CharField(max_length=20, blank=False, unique=True)
    locale = models.CharField(max_length=5, blank=False)
    timezone = models.IntegerField(blank=False)

    def __str__(self):
        return "%s %s;%s" % (self.first_name, self.full_name, self.email)

    class Meta:
        ordering = ('facebook_id',)


class Group(models.Model):
    name = models.CharField(max_length=300, blank=False)
    image = models.ImageField(upload_to=get_unique_image_file_path, null=True)
    creator = models.ForeignKey(User, blank=False, related_name='creator')
    status = models.CharField(choices=GROUP_STATUS,
                              default='active',
                              max_length=10,
                              blank=False)

    def __str__(self):
        return "%s;%s;%s" % (self.name, self.creator, self.status)

    class Meta:
        ordering = ('status', )
        unique_together = (("creator", "name"),)


class Bill(models.Model):
    name = models.CharField(blank=False, max_length=300)
    description = models.CharField(blank=False, max_length=500)
    group = models.ForeignKey(Group, blank=False)
    receipt_image = models.ImageField(upload_to=get_unique_image_file_path, null=True)
    amount = models.FloatField(blank=False)
    currency = models.CharField(blank=False,
                                default='CA',
                                max_length=3,
                                choices=PAYMENT_CURRENCY)
    deadline = models.DateTimeField(blank=False)

    def __str__(self):
        return "%s;%s;%s" % (self.name, self.description, self.group)

    class Meta:
        ordering = ('amount', )


class BillUser(models.Model):
    bill = models.ForeignKey(Bill, blank=False, null=True, related_name='bill')
    amount = models.FloatField(blank=False, null=True)
    member = models.ForeignKey(User, blank=False, related_name='member')
    relation = models.CharField(choices=BILL_RELATION,
                                max_length=10,
                                blank=False,
                                default='debtor')
    status = models.CharField(choices=PAYMENT_STATUS,
                              max_length=10,
                              blank=False,
                              default='not paid')

    def __str__(self):
        return "%s;%s;%s;%s" % (self.bill, self.member, self.relation, self.status)

    class Meta:
        ordering = ('member', )


class GroupUser(models.Model):
    user = models.ForeignKey(User, blank=False, related_name='user')
    group = models.ForeignKey(Group, blank=False, related_name='group')
    administrator = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return "%s;%s;%s" % (self.user, self.group, self.administrator)

    class Meta:
        ordering = ('user', )
        unique_together = (("user", "group"),)