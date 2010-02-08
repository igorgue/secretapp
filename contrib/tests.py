__test__ = {"doctest": """

# 
# These are wrong. Re-building permissions. Waiting for spec.
# 


# building test objects
>>> from django.contrib.auth.models import User
>>> staff = User.objects.create(username='staff', password='x', is_staff=True)
>>> ordinary = User.objects.create(username='ord', password='x')
>>> other = User.objects.create(username='oth', password='x')

>>> from secret.models import Secret
>>> staff_secret = Secret.objects.create(created_by=staff, title='s')
>>> ordinary_secret = Secret.objects.create(created_by=ordinary, title='o')

# first check
>>> Secret.objects.all()
[<Secret: s>, <Secret: o>]



### UserContent.mark_deleted

# only staff can mark as deleted
>>> staff_secret.mark_deleted(ordinary).deleted
False
>>> staff_secret.mark_deleted(staff).deleted
True


# and owners of that object
>>> ordinary_secret.mark_deleted(other).deleted
False
>>> ordinary_secret.mark_deleted(staff).deleted
True
>>> ordinary_secret.deleted = False     #reset
>>> ordinary_secret.mark_deleted(ordinary).deleted
True



### UserContentManager

# staff can view and edit everything
>>> Secret.objects.viewable(staff).all()
[<Secret: s>, <Secret: o>]
>>> Secret.objects.editable(staff).all()
[<Secret: s>, <Secret: o>]

# owners can view and edit anything
>>> Secret.objects.viewable(ordinary).all()
[<Secret: o>]
>>> Secret.objects.editable(ordinary).all()
[<Secret: o>]

# other people can do nothing
>>> Secret.objects.viewable(other).all()
[]
>>> Secret.objects.editable(other).all()
[]
"""}
