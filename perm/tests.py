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
>>> Secret.objects.editable(user).filter(title='test')
[<Secret: test>]

# owners can edit their secrets
>>> Secret.objects.editable(owner).filter(title='test')
[<Secret: test>]

# members can't do anything
>>> Secret.objects.editable(member).filter(title='test')
[]

# owners and superusers can delete (same as edit permissions)
>>> secret.mark_deleted(user).deleted
True

# superusers can see deleted objects
>>> Secret.objects.viewable(user).filter(title='test')
[<Secret: test>]

# owners cannot see deleted items
>>> Secret.objects.viewable(owner).filter(title='test')
[]

# normal members cannot see deleted items
>>> Secret.objects.viewable(member).filter(title='test')
[]

"""}





