from django import forms
from django.core.urlresolvers import reverse
from discussion.models import Discussion
from perm.forms import UserContentForm
from utilz.search import SearchForm
from models import *


# When adding to this list.
#   1. Need to add template
#   2. Need to update solr schema (incl restart)
#   3. Need to reindex solr
SECRET_RENDER_TEMPLATES = ('list', 'photo', 'location')
SECRET_RENDER_FOLDER = 'secret/render/%s.html'
SORT_ORDER = (
                ('created desc', 'Newest'),
                ('created asc', 'Oldest'),
            )
class SecretSearchForm(SearchForm):
    # choose a template
    templates   = SECRET_RENDER_TEMPLATES
    template    = forms.ChoiceField(choices=[(s,s) for s in SECRET_RENDER_TEMPLATES], required=False)
    
    # sort
    sort        = forms.ChoiceField(choices=SORT_ORDER, required=False)
    
    # text
    title       = forms.CharField(required=False)
    text        = forms.CharField(required=False)
    
    # location (maps)
    location_fields = ('north', 'south', 'east', 'west')
    location    = forms.CharField(required=False)
    south       = forms.FloatField(required=False)
    north       = forms.FloatField(required=False)
    west        = forms.FloatField(required=False)
    east        = forms.FloatField(required=False)
    
    class Meta(SearchForm.Meta):
        model = Secret
        url_name = 'search_secrets'
        default_template = 'list'
        default_sort = SORT_ORDER[0][0]
        results_per_page = 10
    
    def render_template(self):
        return self.Meta.query_dict.get('template', self.Meta.default_template)
    
    def template_url(self, template):
        """ Returns the url to change the template but keep the same search critieon """
        q = self.Meta.query_dict.copy()
        q['template'] = template
        return "?%s" % q.urlencode()
    
    def save(self):
        # build vars
        data = self.cleaned_data
        queries = [self.base_query]
        
        # searching only the title field
        if 'title' in data and data['title']:
            queries.append("(title:(%s) OR title:(%s*))" % (data['title'], data['title']))
        
        # searching any text field's (may extend to comments)
        if 'text' in data and data['text']:
            text = data['text']
            queries.append("(title:(%s)^2 OR location:(%s) OR description:(%s))"\
                                                                % (text, text, text))
        
        # do quick check has all fields (ugly)
        lcount = 0
        for f in self.location_fields:
            if f in data and data[f]:
                lcount += 1
        if lcount == 4:
            queries.append("(latitude:[%s TO %s] AND longitude:[%s TO %s])"\
            % (data['south'], data['north'], data['west'], data['east']))
        
        # return
        return self.get_results(" AND ".join(queries))



class SecretForm(UserContentForm):
    class Meta:
        model = Secret
        fields = ('title', 'location', 'latitude', 'longitude', 'description', 'url', 'google_reff')
    
    def set_url(self, secret=None):
        # handling data input
        if hasattr(secret, 'pk') and secret.pk:
            secret_id = secret.pk
        else:
            secret_id = None
        
        # handle options
        if secret_id:
            self.action_url = reverse('edit_secret', kwargs={'pk': secret_id })
        else:
            self.action_url = reverse('new_secret')
        return self
