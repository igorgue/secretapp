from django.contrib.auth.models import User
from django.db import models

class UserSettings(models.Model):
    """
    Stores extra information about the user
    """
    user = models.ForeignKey(User)
    publish_to_wall = models.BooleanField(default=True)


def cache_as_var(func):
    """
    This caches the result of the given function
    onto the object as a private variable.
    Useful if the calculation is expensive.
    
    NOTE: this isn't passing self var through...
        clearly need to do more results.
        Anyone better than me to fix?
    
    """
    def wrapper(self, *args, **kwargs):
        key = '_cache__%s' % func.func_name
        if not hasattr(self, key):
            return setattr(self, key, func(*args, **kwargs))
        return getattr(self, key)
    return wrapper


# Functions which we want appended to the User object
def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    return reverse('view_profile', kwargs={'pk': self.pk })

def get_time_since_joined(self):
    from perm.tools import calculate_time_since
    return calculate_time_since(self.date_joined)    

def get_settings(self):
    if not hasattr(self, '_settings'):
        self._settings, new = UserSettings.objects.get_or_create(user=self)
    return self._settings

def __get_items(self, Model):
    key = '_cache__%s' % Model._meta.app_label
    if not hasattr(self, key):
        setattr(self, key, Model.viewable.filter(created_by=self))
    return getattr(self, key)

def secrets(self):
    from secret.models import Secret
    return __get_items(self, Secret)

def secret_count(self):
    from secret.models import Secret
    return Secret.viewable.filter(created_by=self).count()

def proposals(self):
    from comment.models import Proposal
    return Proposal.viewable.filter(discussion_comment__created_by=self).order_by("-discussion_comment__created_at")

def proposal_count(self):
    from comment.models import Proposal
    return Proposal.viewable.filter(discussion_comment__created_by=self).count()

def discussions(self):
    from discussion.models import Discussion
    #return __get_items(self, Discussion)
    return Discussion.viewable.filter(created_by=self).order_by("-created_at")

def discussion_count(self):
    from comment.models import Discussion
    return Discussion.viewable.filter(created_by=self).count()

def agreements(self):
    from comment.models import Agreement
    #return __get_items(self, Agreement)
    return Agreement.viewable.filter(created_by=self).order_by("-created_at")

def agreement_count(self):
    from comment.models import Agreement
    return Agreement.viewable.filter(created_by=self).count()

def agreed_with_me_count(self):
    from comment.models import Agreement
    return Agreement.viewable.filter(proposal__discussion_comment__created_by=self).count()

def favourites(self):
    from secret.models import FavouriteSecret
    return __get_items(self, FavouriteSecret)

@property
def name(self):
    return "%s %s" % (self.first_name, self.last_name[:1])

@property
def name_alt(self):
    return self.name

def get_facebook(self):
    if not hasattr(self, '_facebook'):
        from socialauth.models import FacebookUserProfile
        try:
            self._facebook = FacebookUserProfile.objects.filter(user=self).latest('pk')
        except:
            self._facebook = None
    return self._facebook

@property
def is_facebook(self):
    return True if self.get_facebook() else False

class ProfileImage(object):
    def __init__(self, user):
        # defaults
        self.big = 'http://static.ak.connect.facebook.com/pics/d_silhouette.gif'
        self.medium = 'http://static.ak.connect.facebook.com/pics/s_silhouette.gif'
        self.small = 'http://static.ak.connect.facebook.com/pics/t_silhouette.gif'
        # facebook
        fb = user.get_facebook()
        if fb:
            if fb.profile_image_url_big:
                self.big = fb.profile_image_url_big
            if fb.profile_image_url:
                self.medium = fb.profile_image_url
            if fb.profile_image_url_small:
                self.small = fb.profile_image_url_small

def profile_image(self):
    if not hasattr(self, '_profile_image'):
        self._profile_image = ProfileImage(self)
    return self._profile_image

# Actually append these functions on the user object
__user_augments__ = (
    'get_time_since_joined',
    'get_absolute_url',
    'get_settings',
    'get_facebook',
    'is_facebook',
    'name',
    'name_alt',
    
    'profile_image',
    'secrets',
    'proposals',
    'discussions',
    'agreements',
    'favourites',
    
    'secret_count',
    'agreement_count',
    'agreed_with_me_count',
    'proposal_count',
    'discussion_count',
)

User.get_settings = get_settings

for attr in __user_augments__:
    # doesn't play well with wrappers
    setattr(User, attr, locals()[attr])
    



