from django import forms
from django.http import HttpRequest, QueryDict
from django.core.urlresolvers import reverse
import solango

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
    
    """
    REQUIRED    = ('model', 'url_name')
    page        = forms.IntegerField(initial=1, widget=forms.HiddenInput)
    
    class Meta:
        method = 'GET'
        results_per_page = 10
    
    def __init__(self, GET=None, *args, **kwargs):
        # sort out data types
        if isinstance(GET, dict):
            QD = QueryDict('').copy()
            QD.update(GET)
            GET = QD
        
        # update Meta
        Mota = super(SearchForm, self).__thisclass__.Meta
        for attr in dir(Mota):
            if not hasattr(self.Meta, attr):
                setattr(self.Meta, attr, getattr(Mota, attr))
        
        # error checking for needed fields
        for r in self.REQUIRED:
            if not hasattr(self.Meta, r):
                raise AttributeError, "Must define %s in Meta of SearchForm" % r
        
        # set the url
        self.Meta.url = reverse(self.Meta.url_name)
        # used in pagination urls later
        self.Meta.query_dict = GET
        # super init
        super(SearchForm, self).__init__(GET, *args, **kwargs)
    
    @property
    def base_query(self):
        """ The starter query to make sure you get the right model, not deleted etc etc... """
        return 'model:(+%s) ' % solango.solr.get_model_key(self.Meta.model)
    
    def get_results(self, query):
        """ Connects to solr and actually runs sort """
        return solango.connection.select(q=query, sort=self.cleaned_data.get('sort', ''))
    
    def paginate(self, results):
        """
        Solango's built in page system is designed to work with its crappy search views.
        This provides a more generic system and usage.
        
        Template example:
            
            {% if results.pages %}
                {% if results.previous %}<a href="{{ results.previous }}">previous</a>{% endif %}
                {% for page in results.pages %}
                        {% ifequal page results.page %}
                            <b class="page">{{page}}</b>
                        {% else %}
                            <a href="{{results.page.url}}">{{page}}</a>
                        {% endifequal %}
                {% endfor %}
                {% if results.next %}<a href="{{ results.next }}">next</a>{% endif %}
            {% endif %}
            
        """
        # detect the correct page
        page = 1
        if hasattr(self, 'cleaned_data'):
            page = self.cleaned_data.get('page', page)
        
        # create path
        qd = self.Meta.query_dict
        
        class Page(object):
            def __init__(self, id):
                self.id = id
                qd['page'] = id
                self.url = "?%s" % qd.urlencode()
            def __unicode__(self):
                return u"%s" % self.id
        
        # choose the correct selection
        results.selection = results.documents[(page-1)*self.Meta.results_per_page: page*self.Meta.results_per_page]
        
        # work out page links
        results.page = Page(page)
        
        pages = []
        page_count = int(math.ceil(results.count/self.Meta.results_per_page)+1)
        for p in xrange(1, page_count):
            pages.append(Page(p))
        results.pages = pages
        
        results.previous = Page(page-1) if page > 1 else None
        results.next = Page(page+1) if page < page_count else None
        
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








