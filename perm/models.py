from django.contrib.auth.models import User
from django.db import models
from tools import *
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

class UserContentManager(models.Manager):
    def get_query_set(self):
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
    
    viewable        = UserContentManager()
    objects         = models.Manager()
    
    # see above for details
    # make edit_permission default to highest
    edit_permission = 'Secretary'
    
    class Meta:
        abstract = True
    
    def __user_can(self, user):
        self._is_editable = user.permission_level >= \
            permission_level(self.edit_permission) or self.created_by == user
        self._is_viewable = not self.deleted or \
            (user is not None and user.is_superuser)
        return self
    
    def user_can_edit(self, user):
        # editable if has permissions or is owner
        self.__user_can(user)
        return self._is_editable
    
    def user_can_view(self, user=None):
        # viewable if not deleted or are superuser
        self.__user_can(user)
        return self._is_viewable
    
    def _is_perm(self, var):
        uvar = '_%s' % var
        if hasattr(self, uvar):
            return getattr(self, uvar)
        else:
            raise AttributeError, \
            "Please run `user_can` before accessing %s" % var
    
    @property
    def is_editable(self):
        return self._is_perm('is_editable')
    
    @property
    def is_viewable(self):
        return self._is_perm('is_viewable')
    
    @property
    def deleted_by(self):
        # handles related_name error (see above)
        if self.deleted_by_id:
            return User.objects.get(pk=self.deleted_by_id)
        else:
            return None
    
    def mark_deleted(self, user):
        "marks an object as deleted - if have correct permissions"
        if self.user_can_edit(user):
            self.deleted = True
            self.deleted_at = datetime.datetime.now()
            # would make this nicer - but only used for refference in emergency
            self.deleted_by_id = user.id
            self.save()
        return self


