from django.db import IntegrityError

from test_extensions.django_common import DjangoCommon
from django.contrib.auth.models import User

from comment.models import *
from secret.models import Secret

class ModelTests(DjangoCommon):
    def setUp(self):
        FavouriteSecret.objects.all().delete()
        Secret.objects.all().delete()
        
        if not User.objects.all():
            from django.core.management import call_command
            call_command("createsuperuser", username='admin', 
                         email='admin@foobar.com', interactive = False)
            self.user = User.objects.all()[0]
            
        Secret(title='foobar', description='something', 
               created_by = self.user).save()
        
    def test_secret(self):
        s = Secret.objects.all()[0]
        self.assertEquals(s.title, 'foobar')    