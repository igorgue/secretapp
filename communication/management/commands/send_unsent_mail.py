from django.core.management.base import NoArgsCommand
 
from communication.models import Communcation
 
class Command(NoArgsCommand):
    help = "Emit queued notices."
    
    def handle_noargs(self, **options):
        # TODO: raise failure if these are not sending
        Communication.objects.send_unsent()