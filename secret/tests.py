from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from models import *

class SecretTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='x')
        self.client.login(username='user', password='x')
    
    def test_search(self):
        # TODO
        pass
        
    def test_view(self):
        
        pass
    
    def test_edit(self):
        
        pass
    