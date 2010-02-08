from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from utils import *
import datetime

"""
Notes on permissions:
    There are a few groups (with ridiculous names)
        
    1. Secretary (group #1)
        Seneschal +
        Appoint seneschals
    
    2. Seneschal (group #2)
        Keeper +
        Suspend users
        Edit/Delete discussions
        Appoint keepers
    
    3. Keeper (group #3)
        Member +
        Edit/Delete secrets
        Edit/Delete posts within discussion
    
    4. Member (user.is_active)
        Vistor +
        Discuss
        Post secrets
        Like secrets
        Delete own posts
    
    5. Visitor (not user.is_authenticated)
        Read only

In summary for objects:
    To create
        Requires you to be a `Member`
    
    To edit/delete
        Owners can edit/delete
        Each object has its own group permission level [PERMISSION_GROUP]
    
    To view
        Anyone can view anything which is not deleted
        Only superusers can view deleted items

The user logic (permission upscalling and group assignment)
will then be handled according to the above spec.

The users group level is assigned and saved in a middleware.

"""

class HandleManager(models.Manager):
    """ Adds extra cool helpers. See tests.py """
    def get_or_404(self, *args, **kwargs):
        # this isn't ideal, should return a PermissionError in some usecases
        return get_object_or_404(self.model, *args, **kwargs)


class UserContentManager(HandleManager):
    """ Allow permission management. See tests.py """
    
    def editable(self, user):
        # staff can see anything
        if user.permission_level >= permission_level(self.model.edit_permission):
            return self.get_query_set()
        # otherwise you have to be the owner
        else:
            return self.filter(created_by=user)
    
    def viewable(self, user=None):
        # superusers can see anything
        if user and user.permission_level >= permission_level('Secretary'):
            return self.get_query_set()
        # otherwise you cannot see deleted items
        else:
            return self.filter(deleted=False)


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
    
    # see above for details
    # make edit_permission default to highest
    edit_permission = 'Secretary'
    
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
        if user.permission_level >= permission_level(self.edit_permission):
            self.deleted = True
            self.deleted_at = datetime.datetime.now()
            # would make this nicer - but only used for refference in emergency
            self.deleted_by_id = user.id
            self.save()
        return self


