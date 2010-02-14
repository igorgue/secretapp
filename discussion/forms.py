from django import forms
from perm.forms import UserContentForm
from utilz.search import SearchForm
from models import *

class DiscussionSearchForm(SearchForm):
    # sort
    sort    = forms.ChoiceField(choices=(
                    ('created desc', 'Newest'),
                    ('updated desc', 'Activity'),
                    ('comments desc', 'Most Posts'),
                    ('secrets desc', 'Most Secrets'),
                ), required=False)
    
    # text searches
    title   = forms.CharField(required=False)
    text    = forms.CharField(required=False)
    
    class Meta(SearchForm.Meta):
        model = Discussion
        url_name = 'search_discussions'
        results_per_page = 20
    
    def save(self):
        # build vars
        data = self.cleaned_data
        queries = [self.base_query]
        
        # searching only the title field
        if 'title' in data and data['title']:
            queries.append("(title:(%s)^3 OR title:(%s*))" % (data['title'], data['title']))
        
        # searching for any text
        if 'text' in data and data['text']:
            queries.append("(title:(%s)^10 OR text:(%s)^3 OR blob:(%s))"\
                            % (data['text'], data['text'], data['text']))
        # return
        return self.get_results(" AND ".join(queries))


class DiscussionForm(UserContentForm):
    class Meta:
        model = Discussion
        fields = ('title', 'text', 'tags')
