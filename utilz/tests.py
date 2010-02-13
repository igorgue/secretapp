__test__ = {'doctest': """

##
## safe_title
##
>>> from utilz.manipulators import safe_title
>>> safe_title("Where can I buy good cheese ")
'Where-can-I-buy-good-cheese'
>>> safe_title("Is 12 fish  enough $!}{} pur-ple monkey")
'Is-12-fish-enough-pur-ple-monkey'


"""}