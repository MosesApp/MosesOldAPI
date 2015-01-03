import uuid
from django.db import models
from rest_framework.exceptions import ValidationError
from MosesWebservice.settings import GROUP_STATUS, PAYMENT_STATUS, IMAGE_FOLDER
import os


def get_unique_image_file_path(instance=None, filename='dummy.jpg'):
    """
    function to determine where to save images.  assigns a uuid (random string) to each and places it
    in the images subdirectory below media.  by default, we assume the file is a .jpg
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(IMAGE_FOLDER, filename)


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
    owner = models.ForeignKey(User, blank=False, related_name='owner')
    status = models.CharField(choices=GROUP_STATUS,
                              default='active',
                              max_length=10,
                              blank=False)

    def __str__(self):
        return "%s;%s;%s" % (self.name, self.owner, self.status)

    class Meta:
        ordering = ('status', )
        unique_together = (("owner", "name"),)


class Bill(models.Model):
    group = models.ForeignKey(Group)
    receipt_image = models.ImageField(upload_to=get_unique_image_file_path, null=True)
    receiver = models.ForeignKey(User, blank=False, related_name='receiver')
    debtor = models.ForeignKey(User, blank=False, related_name='debtor')
    amount = models.IntegerField(blank=False)
    deadline = models.DateTimeField(blank=False)
    status = models.CharField(choices=PAYMENT_STATUS,
                              default='not paid',
                              max_length=10,
                              blank=False)

    def save(self, *args, **kwargs):
        if self.receiver != self.debtor:
            super(Bill, self).save(*args, **kwargs)
        else:
            raise ValidationError("Receiver and Debtor cannot be the same person")

        if self.amount > 0:
            super(Bill, self).save(*args, **kwargs)
        else:
            raise ValidationError("Bill amount must be higher than zero")

    def __str__(self):
        return "%s;%s;%s" % (self.receiver, self.debtor, self.status)

    class Meta:
        ordering = ('amount', )


class GroupUser(models.Model):
    user = models.ForeignKey(User, blank=False, related_name='user')
    group = models.ForeignKey(Group, blank=False, related_name='group')

    def __str__(self):
        return "%s;%s" % (self.user, self.group)

    class Meta:
        ordering = ('user', )
        unique_together = (("user", "group"),)