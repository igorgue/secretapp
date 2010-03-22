from django import forms
from django.core.urlresolvers import reverse
from perm.forms import UserContentForm
from utilz.search import SearchForm
from models import *

SORT_ORDERS = (
                ('updated desc', 'Most Active'),
                ('created desc', 'Most Recent'),
                ('comments desc', 'Most Posts'),
                ('secrets desc', 'Most Secrets'),
                ('secrets asc', 'Fewest Secrets'),
            )

SORT_MAPPING = {'latest':'updated desc', 'popular':'secrets desc', 'unanswered':"secrets asc" }

USER_SORT_ORDERS = (
                ('latest', 'Latest'),
                ('popular', 'Popular'),
                ('unanswered', 'Unanswered'),
            )

class DiscussionSearchForm(SearchForm):
    # sort
    sort    = forms.ChoiceField(choices=SORT_ORDERS, required=False)
    usort    = forms.ChoiceField(choices=USER_SORT_ORDERS, required=False)
    
    # text searches
    title   = forms.CharField(required=False)
    text    = forms.CharField(required=False)
    
    class Meta(SearchForm.Meta):
        model = Discussion
        url_name = 'search_discussions'
        results_per_page = 10
        default_sort = SORT_ORDERS[0][0]
        cheeky = False    
    
    def clean_sort(self):
        data = self.cleaned_data['sort']
        if 'usort' in self.data:
            usort = self.data['usort']
            if usort in SORT_MAPPING:
                data = SORT_MAPPING[usort]
            else:
                data = self.Meta.default_sort

        return data
    
    def get_available_sort_orders(self):
        return USER_SORT_ORDERS
    
    def save(self):
        import re
        # build vars
        data = self.cleaned_data
        queries = [self.base_query]
        
        # searching only the title field
        if 'title' in data and data['title']:
            title = data['title']
            queries.append("(title:(%s)^3 OR title:(%s*))" % (title, title))
        
        # searching for any text
        if 'text' in data and data['text']:
            text = data['text']
            queries.append("(title:(%s)^3 OR text:(%s)^3 OR blob:(%s))"\
                            % (text,text,text))
        # return
        return self.get_results(" AND ".join(queries))


class DiscussionForm(UserContentForm):
    tags = forms.CharField(required=False, widget=forms.TextInput)
    facebook_publish = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = Discussion
        fields = ('title', 'text', 'tags')
    
    def set_url(self, new=True):
        if new:
            self.action_url = reverse('new_discussion')
        return self



