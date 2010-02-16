import datetime

from django.db import models


class UrlCache(models.Model):
    path = models.CharField(max_length = 255, db_index = True)
    value = models.TextField(blank = True, editable=False)
    content_type = models.CharField(max_length=255, blank=True, editable=False)
    expire_after = models.IntegerField(
        default = 5 * 60, help_text = "In seconds"
    )
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def expires(self):
        return self.updated + datetime.timedelta(seconds = self.expire_after)

    def was_updated(self):
        # We use this in the changelist view instead of just 'updated' 
        # because doing so forces ISO representation which includes seconds
        return self.updated

    def current_value(self):
        if self.value:
            return self.value[0:30] + '...'
        else:
            return ''

    def invalidate_now(self):
        return '<a href="?invalidate=%s">Clear cache</a>' % self.path
    invalidate_now.allow_tags = True

    def __unicode__(self):
        return '%s, expires after %d seconds' % (self.path, self.expire_after)

    def is_usable(self):
        "An item is usable if its value is not blank and it has not expired"
        if not self.value:
            return False
        return self.expires() > datetime.datetime.now()
