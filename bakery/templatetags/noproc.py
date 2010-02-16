""" part of the two-pass caching engine. """
from django import template
register = template.Library()

BLOCK_END = 'endnoproc'
BLOCK_MARKS = {
    template.TOKEN_TEXT: ('', ''),
    template.TOKEN_VAR: ('{{', '}}'),
    template.TOKEN_BLOCK: ('{%', '%}'),
    template.TOKEN_COMMENT: ('{#', '#}'),
}

def noproc(parser, token):
    text = []
    
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == template.TOKEN_BLOCK and token.contents == BLOCK_END:
            tn = template.TextNode(u''.join(text))
            return tn
        start, end = BLOCK_MARKS[token.token_type]
        text.append(u'%s%s%s' % (start, token.contents, end))
    parser.unclosed_block_tag(BLOCK_END)
    
raw = register.tag(noproc)
