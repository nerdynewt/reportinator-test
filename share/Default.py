import pypandoc
import sys

section=sys.argv[1]

filters = ['pandoc-xnos']
pdoc_args = ['--wrap=preserve']
# print("===" + section)
# print("sdfasdfafsas444444444444444444444444444444444444444444")
print(pypandoc.convert_text(section, to='latex', format='markdown-auto_identifiers', extra_args=pdoc_args, filters=filters))
# print(pypandoc.convert_text(section, 'latex', format='md'))
