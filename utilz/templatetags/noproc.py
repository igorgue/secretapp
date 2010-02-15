""" part of the two-pass caching engine. """
from django import template
register = template.Library()

TAG_BLOCKS = {
    template.TOKEN_TEXT: ('', ''),
    template.TOKEN_VAR: ('{{', '}}'),
    template.TOKEN_BLOCK: ('{%', '%}'),
    template.TOKEN_COMMENT: ('{#', '#}'),
}
BLOCK_END = "endnoproc"

def _mkelement(token):
    start, end = TAG_BLOCKS[token.token_type]
    return u'%s%s%s' % (start, token.contents, end)

class BlockEnd(Exception): pass
def _continueParse(token):
    if token.token_type == template.TOKEN_BLOCK and \
        token.contents == BLOCK_END:
        raise BlockEnd
    return True

def nocache(parser, token):
    """ Template content surrounded by {% noproc %} {% endnoproc %} 
will be returned un-molested thus allowing contents to be passed into a cache for
subsequent parsing by template engine in a second pass"""
    try:
        output = [ _mkelement(token) for token in parser.tokens 
                  if _continueParse(token)
                  ]
    except BlockEnd:
        return template.TextNode(u''.join(output))
    
    parser.unclosed_block(BLOCK_END)
    
raw = register.tag(nocache)
    
