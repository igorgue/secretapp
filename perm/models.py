from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from tools import *
from django.conf import settings
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
        return super(UserContentManager, self).get_query_set().filter(deleted=False)


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
    approved        = models.BooleanField(default=False, help_text="Has been checked by an admin")
    ip              = models.IPAddressField(blank=True, null=True)
    
    viewable        = UserContentManager()
    objects         = models.Manager()
    
    spamflags       = generic.GenericRelation("SpamFlag")
    
    # see above for details
    # make edit_permission default to highest
    edit_permission = 'Secretary'
    
    class Meta:
        abstract = True
    
    def __user_can(self, user):
        self.read_by = user
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
    
    @property
    def deleted_by_creator(self):
        return self.deleted_by_id == self.created_by_id
    
    def mark_deleted(self, user):
        "marks an object as deleted - if have correct permissions"
        if self.user_can_edit(user):
            self.deleted = True
            self.deleted_at = datetime.datetime.now()
            # would make this nicer - but only used for refference in emergency
            self.deleted_by_id = user.id
            self.save()
        return self
    
    @property
    def spam_count(self):
        return self.spamflags.all().count()
    
    @property
    def is_spam(self):
        """ Return TRUE if this object is now considered SPAM"""
        return self.spam_count > settings.SPAM_THRESHOLD

    def mark_spam(self, user):
        """adds a spam flag to this object. An IntegrityError will be raised
if a user flags a given object more than once. This is deliberate: view logic
can use the exception raised to drive messaging to the user."""
        SpamFlag(flagged_by=user, spammed_object=self).save()


class SpamFlag(models.Model):
    """ Record of someone flagging something as Spam. """
    flagged_by      = models.ForeignKey(User)
    flagged_at      = models.DateTimeField(auto_now_add=True)
    
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    spammed_object  = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return("%s : %s" % (self.object_id, str(self.spammed_object)))
    
    class Meta:
        unique_together = (('flagged_by', 'content_type', 'object_id'),)


