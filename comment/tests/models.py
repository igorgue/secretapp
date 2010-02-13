from django.db import IntegrityError

from test_extensions.django_common import DjangoCommon
from django.contrib.auth.models import User

from comment.models import *

class ModelTests(DjangoCommon):
    def setUp(self):
        pass
    
    def test_something(self):
        pass