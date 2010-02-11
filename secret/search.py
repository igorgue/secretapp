from django.template.loader import render_to_string
from utils.search import SearchDocument
from models import Secret
from forms import *
import solango

class sFloatField(solango.fields.Field):
    """ need to define a sfloat field to do range queries """
    dynamic_suffix = "f"
    type = "sfloat"
    
    def clean(self):
        if not isinstance(self.value, float):
            self.value = float(self.value)


class SecretDocument(SearchDocument):
    # title / text
    title       = solango.fields.TextField(indexed=True, stored=True)
    description = solango.fields.TextField(indexed=True, stored=True)
    url         = solango.fields.TextField(indexed=True, stored=True)
    
    # location
    location    = solango.fields.TextField(indexed=True, stored=True)
    latitude    = sFloatField(indexed=True, stored=True)
    longitude   = sFloatField(indexed=True, stored=True)
    
    def render(self, template):
        return self.data_dict["render_%s" % template]
    
    @classmethod
    def add_renders(self):
        # render func
        def render_func(template):
            # gets self, instance
            return lambda s,i: render_to_string(SECRET_RENDER_FOLDER % template, {'secret': i})
        
        # save for each language
        for t in SECRET_RENDER_TEMPLATES:
            # Ugly hack to dynamically add fields onto SearchDocument
            name = 'render_%s' % t
            # need to create a new field instance for each template rendering
            field = solango.fields.TextField(indexed=True, stored=True)
            # name the field and save to base_fields
            field.name = name
            SecretDocument.base_fields[name] = field
            # add transform accessor for save
            setattr(SecretDocument, "transform_%s" % name, render_func(t))
        return self

SecretDocument.add_renders()