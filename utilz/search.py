from django import forms
from django.http import HttpRequest, QueryDict
from django.core.urlresolvers import reverse
import solango
import math

class Page(object):
    def __init__(self, id, qd):
        self.id = id
        qd['page'] = id
        self.url = "?%s" % qd.urlencode()
    
    def __unicode__(self):
        return u"%s" % self.id
    
    def __str__(self):
        return self.__unicode__()
    
    def __eq__(self, o):
        if isinstance(o, Page):
            return self.id == o.id
        elif isinstance(o, (int,str,unicode,float)):
            try:
                return self.id == int(o)
            except:
                pass
        raise NotImplementedError, "%s was %s. Please supply a `Page` or `int`" % (o, type(o))
    
    def __ne__(self, other):
        return not self.__eq__(other)


class SearchDocument(solango.SearchDocument):
    """
    Adds additional helps to the standard SearchDocument.
    """
    deleted = solango.fields.BooleanField(indexed=True, stored=True)
    
    def is_indexable(self, instance):
        """ Only index the unit if it has been approved """
        return not instance.deleted


class SearchForm(forms.Form):
    """
    Abstract handler for Search.
    
    Takes as first argument:
        Major change. Takes request, not request.GET!
    
    Meta needs arguments...
        model := Model which you are searching for
        url_name := name of search url regex
    
    Meta optional arguments...
        results_per_page [10] := how many to show per page
        max_page_over [5] := how many pages are shown around the selected
    
    """
    REQUIRED    = ('model', 'url_name')
    page        = forms.IntegerField(initial=1, widget=forms.HiddenInput, required=False)
    quantity    = forms.IntegerField(initial=500, widget=forms.HiddenInput, required=False)
    
    class Meta:
        method = 'GET'
        results_per_page = 500
        start_page = 1
        max_page_over = 5
        default_sort = ''
    
    def __init__(self, GET=None, *args, **kwargs):
        # sort out data types
        if isinstance(GET, dict):
            QD = QueryDict('').copy()
            QD.update(GET)
            GET = QD
        
        # error checking for needed fields
        for r in self.REQUIRED:
            if not hasattr(self.Meta, r):
                raise AttributeError, "Must define %s in Meta of SearchForm" % r
        
        # set the url
        self.action_url = reverse(self.Meta.url_name)
        # used in pagination urls later
        self.Meta.query_dict = GET
        # super init
        super(SearchForm, self).__init__(GET, *args, **kwargs)
    
    @property
    def base_query(self):
        """ The starter query to make sure you get the right model, not deleted etc etc... """
        return '{!lucene q.op=AND} model:(+%s) ' % solango.solr.get_model_key(self.Meta.model)
    
    @property
    def start_page(self):
        if hasattr(self, 'cleaned_data') and self.cleaned_data.has_key('page'):
            p = self.cleaned_data['page']
            if p:
                return p
        return self.Meta.start_page
    
    def get_results(self, query):
        """ Connects to solr and actually runs sort """
        if 'sort' in self.cleaned_data and self.cleaned_data['sort']:
            sort = self.cleaned_data['sort']
        else:
            sort = self.Meta.default_sort
        
        results = solango.connection.select(q=query,
                sort = sort,
                rows = self.Meta.results_per_page,
                start = (self.start_page-1)*self.Meta.results_per_page,
                )
        return self.__paginate(results)
    
    def __paginate(self, results):
        """
        Solango's built in page system is designed to work with its crappy search views.
        This provides a more generic system and usage.
        
        Template example:
            
            {% if results.pages %}
                {% if results.previous %}<a href="{{ results.previous.url }}">previous</a>{% endif %}
                {% for page in results.pages %}
                        {% ifequal page results.page %}
                            <b class="page">{{page}}</b>
                        {% else %}
                            <a href="{{page.url}}">{{page}}</a>
                        {% endifequal %}
                {% endfor %}
                {% if results.next %}<a href="{{ results.next.url }}">next</a>{% endif %}
            {% endif %}
            
        """
        # detect the correct page
        page = self.start_page
        
        # create path
        qd = self.Meta.query_dict
        
        # how many search results should be returned on a per search basis
        if 'quantity' in self.cleaned_data and self.cleaned_data['quantity']:
            self.Meta.results_per_page = self.cleaned_data['quantity']
        
        # work out page links
        results.page = Page(page, qd)
        
        pages = []
        page_count = int(math.ceil(results.count/self.Meta.results_per_page)+1)
        results.page_count = page_count
        
        offset = page - self.Meta.max_page_over
        pages_start = offset if offset > 0 else 1
        
        offset = page + self.Meta.max_page_over
        pages_end = offset if offset < page_count else page_count
        
        for p in xrange(pages_start, pages_end+1):
            pages.append(Page(p, qd))
        results.pages = pages
        
        results.previous = Page(page-1, qd) if page > 1 else None
        results.next = Page(page+1, qd) if page < page_count else None
        results.first = Page(1, qd) if not page == 1 else None
        
        results.start_item = ((pages_start-1)*self.Meta.results_per_page) + 1
        end_item = results.start_item + self.Meta.results_per_page - 1
        if end_item > results.count:
            end_item = results.count
        results.end_item = end_item
        
        
        results.gt_onepage = len(results.pages) > 1
        
        return results
    
    def save(self):
        """
        Gets results ... 
        
        Example:
            query = self.base_query
            if 'title' in self.cleaned_data:
                query += " title:(%s) " % self.cleaned_data['title']
            return self.get_results(query)
        
        """
        return self.get_results(self.base_query)








