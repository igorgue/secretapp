from django.core.management.base import NoArgsCommand
from communication.models import Communication
from django.core import mail


class Command(NoArgsCommand):
    help = "Emit queued notices."
    
    def handle_noargs(self, **options):
        # open mail connection
        connection = mail.SMTPConnection()
        
        # collect all unsent mail
        unsent_coms = Communication.objects.unsent()
        messages = []
        
        # build a list of all mail to be sent
        for u in unsent_coms:
            if u.should_send():
                messages.append(u.email_message())
            else:
                u.deleted = True
                u.save()
        
        # try sending and update status of messages
        try:
            connection.send_messages(messages)
        except:
            unsent_coms.update(failed=True)
        else:
            unsent_coms.update(sent=True)
