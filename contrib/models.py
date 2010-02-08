from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
import datetime


class HandleManager(models.Manager):
    """ Adds extra cool helpers. See tests.py """
    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)


class UserContentManager(HandleManager):
    """ Allow permission management. See tests.py """
    
    def editable(self, user):
        # staff can see anything
        if user.is_staff or user.is_superuser:
            return self.get_query_set()
        # otherwise you have to be the owner
        else:
            return self.filter(created_by=user)
    
    def viewable(self, user=None):
        # staff can see anything
        if user.is_staff or user.is_superuser:
            return self.get_query_set()
        # owners can see deleted, everyone else can only see non-deleted
        else:
            return self.filter(models.Q(created_by=user) | models.Q(deleted=False))


class UserContent(models.Model):
    """ An abstract model which deals with permissions around User generated content """
    # See http://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name
    # related_name conflicts. As deleted_by is barely used (only for admin use).
    # no reason to spend alot of time on this...
    created_by      = models.ForeignKey(User)
    deleted_by_id   = models.PositiveIntegerField(blank=True, null=True)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(blank=True, null=True)
    deleted         = models.BooleanField(default=False)
    ip              = models.IPAddressField(blank=True, null=True)
    
    objects         = UserContentManager()
    
    class Meta:
        abstract = True
    
    @property
    def deleted_by(self):
        # handles related_name error (see above)
        if self.deleted_by_id:
            return User.objects.get(pk=self.deleted_by_id)
        else:
            return None
    
    def mark_deleted(self, user):
        "marks an object as deleted - if have correct permissions"
        if user.is_staff or user.is_superuser or user == self.created_by:
            self.deleted = True
            self.deleted_at = datetime.datetime.now()
            # would make this nicer - 
            self.deleted_by_id = user.id
            self.save()
        return self


