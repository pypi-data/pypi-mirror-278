from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

__all__ = ["ResourceLexer"]

class ResourceLexer(RegexLexer):
    name = 'Restrict Framework Resource Language'
    aliases = ['restrict-resources', 'restrict-resource']
    filenames = ['*.resources', '*.resource']
    mimetypes = ["text/x-restrict-resource"]

    tokens = {
        'root': [
            (r'^\s*(versioned\s+)?(party|role|moment|interval|description)', Keyword.Declaration),
            (r'include <[^>]+>', Comment.PreprocFile),
            (r'(optional|page)', Keyword.Declaration),
            (r'<(party|next|previous):(\d+|\*|\?)>', Name.Decorator),
            (r'\b[A-Z][a-zA-Z]+(\(\s*(\d+|\d+\s*,\s*\d+)\s*\))?', Name.Class),
            (r'\b([a-z][a-zA-Z]+)\s*(:)', bygroups(Name.Property, Punctuation)),
            (r'\b([a-z][a-zA-Z]+)\b', Name.Property),
            (r'<entrypoint|description>', Name.Decorator),
            (r'\b(dnc|access|defined)\b', Keyword.Reserved),
            (r'\b(in|is)\b', Operator.Word),
            (r'(<|>|=|\||\*)', Operator),
            (r'\s+', Whitespace),
            (r'\b[a-z]+\b', Name.Variable),
            ('\{', Punctuation),
            ('\}', Punctuation),
            ('\.', Punctuation),
            ('\[', Punctuation),
            ('\]', Punctuation),
            ('\(', Punctuation),
            ('\)', Punctuation),
            (':', Punctuation),
            (',', Punctuation),
        ],
    }


