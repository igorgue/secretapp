from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
import datetime


class HandleManager(models.Manager):
    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)


class UserContentManager(HandleManager):
    """
    >>> from django.contrib.auth.models import User
    >>> staff = User.objects.create(username='staff', password='x', is_staff=True)
    >>> ordinary = User.objects.create(username='ord', password='x', is_staff=False)
    >>> secret = Secret.objects.create()
    # Tests...
    """
    
    def editable(self, user):
        # staff can see anything
        if user.is_staff or user.is_superuser:
            return self.get_query_set()
        # otherwise you have to be the owner
        else:
            return self.filter(user=user)
    
    def viewable(self, user=None):
        # staff can see anything
        if user.is_staff or user.is_superuser:
            return self.get_query_set()
        # owners can see deleted, everyone else can only see non-deleted
        else:
            return self.filter(models.Q(user=user) | models.Q(deleted=False))


class UserContent(models.Model):
    """
    An abstract model which deals with permissions around User generated content
    """
    created_by      = models.ForeignKey(User, related_name='creator')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(blank=True, null=True)
    deleted         = models.BooleanField(default=False)
    deleted_by      = models.ForeignKey(User, blank=True, null=True, related_name='deletor')
    ip              = models.IPAddressField(blank=True, null=True)
    
    objects         = UserContentManager()
    
    class Meta:
        abstract = True
    
    def mark_deleted(self, user=None):
        self.deleted = True
        self.deleted_at = datetime.datetime.now()
        if user:
            self.deleted_by = user
        self.save()
        return self


