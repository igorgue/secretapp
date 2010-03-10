from django.core.management.base import NoArgsCommand
from communication.models import Communication

class FailedToSendMail(Exception):
    pass


class Command(NoArgsCommand):
    help = "Emit queued notices."
    
    def handle_noargs(self, **options):
        successful = Communication.objects.send_unsent()
        if not successful:
            import datetime
            raise FailedToSendMail("Failed to send some messages -- see admin for failed messages")