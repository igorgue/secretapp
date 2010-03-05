from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

SEND_FROM_EMAIL = getattr(settings, 'COMMUNICATION_EMAIL', settings.EMAIL_HOST_USER)


class CommunicationTrigger(models.Model):
    """
    An instance of where a user gets contacted.
    Where these really come in useful is the form.
    See `forms.py` for details
    
    Usage:
        # say at the event insert the following code
        # firstly we get the trigger which when this occurs
        trigger = CommunicationTrigger.objects.get('friend_request')
        
        # top tip here: if you use get_or_create for the trigger
        # this means the database will automatically keep itself upto date
        # warning: may get messy if trigger same communication from two different places
        
        # create a new communication from the trigger
        com = trigger.create_communication(request.user,
                # context to passed to templates
                {'friend': friend },
                # templates to be rendered
                'communication/friend_request/subject.html',
                'communication/friend_request/body.html',
                'communication/friend_request/web.html')
        
        # this send the message in the thread immediately
        # for this to be picked up by cron - simply do not call send_mail
        # if not called, it gets put on the stack for later
        com.send_mail()
        
    """
    name = models.CharField(max_length=250)
    label = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    
    default = models.BooleanField(default=True)
    optional = models.BooleanField(default=True)
    
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def create_communication(self, user, context, subject_template, body_template, web_template=False):
        """
        This creates a new communication.
        """
        com = Communication(user=user, trigger=self)
        # renders the messages
        com.subject = render_to_string(subject_template, context)
        com.body = render_to_string(body_template, context)
        # checks if its to be shown on the web
        if web_template:
            com.web_visable = True
            com.web = render_to_string(body_template, context)
        else:
            com.web_visable = False
        return com.save()


class CommunicationSetting(models.Model):
    user    = models.ForeignKey(User)
    trigger = models.ForeignKey(CommunicationTrigger)
    is_on   = models.BooleanField(default=True)


class CommunicationManager(models.Manager):
    def websafe(self):
        return self.filter(web_visible=True)
    
    def unsent(self):
        return self.filter(sent=False, read=False, failed=False, deleted=False)
    
    def failed(self):
        return self.filter(failed=True, deleted=False)
    
    def __send_mail(self, func_name, *args, **kwargs):
        """
        Runs send_mail on all communications.
        Returns bool if all were successful.
        """
        coms = getattr(Communication.objects, func_name)()
        successful = True
        for com in coms:
            if not com.send_mail(*args, **kwargs):
                successful = False
        return successful
    
    def send_unsent(self, force=False):
        return self.__send_mail('unsent', force)
    
    def resend_failed(self, force=False):
        return self.__send_mail('failed', force)


class Communication(models.Model):
    "A saved correspondance with us and a user"
    user    = models.ForeignKey(User)
    trigger = models.ForeignKey(CommunicationTrigger, help_text="Textual reference. What triggered this notification")
    
    web     = models.TextField(null=False, blank=False)
    subject = models.TextField(null=False, blank=False)
    body    = models.TextField(null=False, blank=False)
    
    sent    = models.BooleanField(default=True)
    read    = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    failed  = models.BooleanField(default=False)
    web_visable = models.BooleanField(default=True)
    
    objects = CommunicationManager()
    
    
    def __unicode__(self, *args, **kwargs):
        return u"%s: %s" % (self.trigger, self.user.name)
    
    
    def send_mail(self, force=False):
        """
        Description:
            Tries to send the notification by email.
            If fails model is marked as `failed` ready to be re-tried later.
        Arguments:
            Bool to force send the mail.
                if force==False, then it will check that the user has a setting which he wants that note
        Returns:
            Bool if is successful
        """
        if CommunicationSetting.objects.filter(user=self.user, trigger=self.trigger, is_on=True).count() > 0:
            try:
                send_mail(self.subject, self.body, SEND_FROM_EMAIL, [user.email], fail_silently=False)
            except:
                self.failed = True
                successful = False
            else:
                self.sent = True
                successful = True
            self.save()
        return successful










