import more_itertools as mit
import itertools as it
import re

args = {'name_contains':"([FOO BAR] | [BASH*BIZ]) & [TISH**TOOSH]"}


# QUERY STRINGS
#   [FOO BAR] 
#   [FOO*BAR]
#   [FOO**BAR] 
#   i[FOO**BAR] 
#   [FOO**BAR] & i[FOO*BAR]
#   [FOO*BAR] | !i[FOO**BAR]
#   ([FOO**BAR] & i[FOO*BAR]) | [BAR BASH]


regex = ""

for i, char in enumerate(args['name_contains']):
    
    if char == '[':
        regex += "(?i)" if args['name_contains'][max(0, i - 1)] == 'i' else "(?-i)"
        regex += "(?=.*"

        mtch_len = args['name_contains'][i:].index(']')
        mtch = args['name_contains'][(i+1):(i + mtch_len)]

        iterator = mit.peekable(mtch)
        for mtch_char in iterator:
            if mtch_char == '*':
                if iterator.peek(' ') == '*':
                    regex += "[^.]*"
                else:
                    regex += ".*"

            else:
                regex += re.escape(mtch_char)

        regex += ")"

    if char in ('|', '(', ')'):
        regex += char

print(regex)