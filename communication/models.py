from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings
from django.db import models
from django.template import RequestContext, loader

SEND_FROM_EMAIL = getattr(settings, 'COMMUNICATION_EMAIL', settings.EMAIL_HOST_USER)

class ActiveTriggerManager(models.Manager):
    def get_query_set(self):
        return super(ActiveTriggerManager, self).get_query_set().filter(active=True)

class CommunicationTrigger(models.Model):
    """
    An instance of where a user gets contacted.
    Where these really come in useful is the form.
    See `forms.py` for details
    
    Usage:
        # say at the event insert the following code
        # firstly we get the trigger which when this occurs
        trigger = CommunicationTrigger.alive.get(name='friend_request')
        
        # top tip here: if you use get_or_create for the trigger
        # this means the database will automatically keep itself upto date
        # warning: may get messy if trigger same communication from two different places
        
        # create a new communication from the trigger
        com = trigger.create_communication( \
                request, request.user,
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
        
        # or call in a cron
        ./manage.py send_unsent_mail
        
    """
    name = models.CharField(max_length=250)
    label = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    
    default = models.BooleanField(default=True, help_text="Sets if opt-in or opt-out. opt-in is default=False.")
    optional = models.BooleanField(default=True, help_text="Sets if user is allowed to change opt-in/out")
    active = models.BooleanField(default=True, help_text="Is this trigger still active?")
    web_visible = models.BooleanField(default=False)
    
    objects = models.Manager()
    alive = ActiveTriggerManager()
    
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def create_communication(self, request, user, context, subject=None, body=None, \
                    subject_template=None, body_template=None, web_template=None):
        """
        This creates a new communication.
        """
        com = Communication(user=user, trigger=self)
        
        # overrides user in context
        context.update({'recipient': user })
        
        # renders
        def render_or_template(line, template, error):
            if line is not None:
                return line
            else:
                if template is not None:
                    return loader.render_to_string(template,
                                context, context_instance=RequestContext(request))
                else:
                    raise ValueError, error
        
        
        # renders the message subject
        com.subject = render_or_template(subject, subject_template,\
                            "Please provide a `subject` or `subject_template`")
        com.body = render_or_template(body, body_template,\
                            "Please provide a `body` or `body_template`")
        
        
        # checks if its to be shown on the web
        if self.web_visible:
            if web_template:
                com.web = loader.render_to_string(web_template, context)
            else:
                raise ValueError, "Expected a `web_template` for trigger `%s`" % self
        return com.save()


class CommunicationSetting(models.Model):
    user    = models.ForeignKey(User, db_index=True)
    trigger = models.ForeignKey(CommunicationTrigger, db_index=True)
    is_on   = models.BooleanField(default=True)


class CommunicationManager(models.Manager):
    def websafe(self):
        return self.filter(trigger__web_visible=True)
    
    def unsent(self):
        return self.filter(sent=False, read=False, failed=False, deleted=False)
    
    def failed(self):
        return self.filter(failed=True, deleted=False)


class Communication(models.Model):
    "A saved correspondance with us and a user"
    user    = models.ForeignKey(User)
    trigger = models.ForeignKey(CommunicationTrigger, help_text="Textual reference. What triggered this notification")
    
    web     = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    body    = models.TextField(null=True, blank=True)
    
    sent    = models.BooleanField(default=False, db_index=True)
    read    = models.BooleanField(default=False, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    failed  = models.BooleanField(default=False, db_index=True)
    
    objects = CommunicationManager()
    
    
    def __unicode__(self, *args, **kwargs):
        return u"%s: %s" % (self.trigger, self.user.name)
    
    def email_message(self):
        return mail.EmailMessage(self.subject, self.body, SEND_FROM_EMAIL, [self.user.email])
    
    def should_send(self):
        # checks email
        u = self.user
        email_ok = u.email and not u.email.strip() == '' and '@proxymail.face' not in u.email
        if email_ok:
            # checks setting
            setting, is_new = CommunicationSetting.objects.get_or_create(\
                                    user=u, trigger=self.trigger, defaults={'is_on':self.trigger.default})
            return setting.is_on
        else:
            return False
    
    def send_mail(self, force=False):
        if self.should_send() or force:
            try:
                message = self.email_message()
                message.send()
            except:
                self.failed = True
                successful = False
            else:
                self.sent = True
                successful = True
            self.save()
            return successful
        else:
            self.deleted = True
            self.save()
            return None










