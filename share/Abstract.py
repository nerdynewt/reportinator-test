import argparse
import sys
import configparse
import os
import csv
import pypandoc

pythonpath = sys.executable
cache_dir=configparse.cfg["cache_dir"]
section=sys.argv[1]
section = "\n".join(section.split("\n")[1:])
filters = ['pandoc-xnos']
pdoc_args = ['--wrap=preserve']
print("\\begin{abstract}\n")
print(pypandoc.convert_text(section, to='latex', format='markdown-auto_identifiers', extra_args=pdoc_args, filters=filters))
print("\\end{abstract}\n")

