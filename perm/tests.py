__test__ = {'doctest': """

##
## permission_level
##
>>> from tools import permission_level
>>> permission_level('Visitor')
0
>>> permission_level('Secretary')
4
>>> permission_level('Secretary') > permission_level('Visitor')
True


##
## calculate_permission_name
##
>>> from tools import calculate_permission_name
>>> from django.contrib.auth.models import User, AnonymousUser, Group

# un_authenticated users are 'Visitor's
>>> calculate_permission_name(AnonymousUser())
'Visitor'

# authed users are 'Member's
>>> user = User.objects.create(username='cpn2', password='x')
>>> calculate_permission_name(user)
'Member'

# otherwise its dependant on the group
>>> group, new = Group.objects.get_or_create(name='Seneschal')
>>> user.groups.add(group)
>>> calculate_permission_name(user)
'Seneschal'

# the highest level group (even when have many)
>>> group, new = Group.objects.get_or_create(name='Secretary')
>>> user.groups.add(group)
>>> calculate_permission_name(user)
'Secretary'


##
## UserContentManager
##

>>> from secret.models import Secret
>>> owner = User.objects.create(username='o', password='x')
>>> member = User.objects.create(username='m', password='x')
>>> secret = Secret.objects.create(created_by=owner, title='test')

# fake out middleware
>>> for u in (user, member, owner):
...    u.permission_level = permission_level(calculate_permission_name(u))

# superusers can edit all secrets
>>> secret.is_editable(user)
True

# owners can edit their secrets
>>> secret.is_editable(owner)
True

# members can't do anything
>>> secret.is_editable(member)
False

# owners and superusers can delete (same as edit permissions)
>>> secret.mark_deleted(user).deleted
True

# superusers can see deleted objects
>>> secret.is_viewable(user)
True

# owners cannot see deleted items
>>> secret.is_viewable(owner)
False

# normal members cannot see deleted items
>>> secret.is_viewable(member)
False

"""}





