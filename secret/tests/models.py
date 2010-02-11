from django.db import IntegrityError

from test_extensions.django_common import DjangoCommon
from django.contrib.auth.models import User

from secret.models import FavouriteSecret
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
        
    def test_add_favourite(self):
        s = Secret.objects.all()[0]
        pass
    
    
# need to look up syntax for spoof requests
#
# once done test:
#
# Create secret, add fave - test exists
# add fave again to same secret - test no new fave created
# delete fave on secret - test flagged deleted
# delete faved again - test no change
# add fave again on same secret - test new fave created, hence one deleted and one new