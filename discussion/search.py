from django.template.loader import render_to_string
from utilz.search import SearchDocument
from models import Discussion
from forms import *
import solango

class DiscussionDocument(SearchDocument):
    # title / text
    title       = solango.fields.TextField(indexed=True, stored=True)
    text        = solango.fields.TextField(indexed=True, stored=True)
    blob        = solango.fields.TextField(indexed=True, stored=True)
    
    # stats
    comments    = solango.fields.IntegerField(indexed=True, stored=True)
    secrets     = solango.fields.IntegerField(indexed=True, stored=True)
    created     = solango.fields.DateTimeField(indexed=True, stored=True)
    updated     = solango.fields.DateTimeField(indexed=True, stored=True)
    
    # render
    render      = solango.fields.TextField(indexed=False, stored=True)
    homerender = solango.fields.TextField(indexed=False, stored=True)
    
    def transform_render(self, instance):
        " Saves the render of the search result "
        return render_to_string('discussion/render/search.html', {'discussion': instance })
    
    def transform_homerender(self, instance):
        " Saves the render of the homepage result "
        return render_to_string('discussion/render/singular.html', {'discussion': instance })
    
    def transform_blob(self, instance):
        " Saves all the discussion content "
        output = ""
        for c in instance.comments():
            output += "\n\n\n%s\n\n\n" % (c.text)
            for s in c.secrets.all():
                output += "\n\n\n%s\n\n\n" % (s.title)
        return output
    
    def transform_comments(self, instance):
        " Most number of discussions "
        return instance.comment_count
    
    def transform_secrets(self, instance):
        " Most number of secret proposals "
        return instance.proposal_count
    
    def transform_created(self, instance):
        " When the discussion was created "
        return instance.created_at
    
    def transform_updated(self, instance):
        " Last time the discussion was commented on - or falls back to when it was created "
        return instance.updated_at


solango.register(Discussion, DiscussionDocument)