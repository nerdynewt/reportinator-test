import yaml
import sys

configpath=sys.argv[2]

with open (configpath, "r") as ymlfile:
    cfg=yaml.safe_load(ymlfile)

header = """
\\documentclass{%s}
\\begin{document}
\\title{%s}
\\author{%s\\thanks{%s}}
\\date{\\today}
\\maketitle
""" % (cfg["style"], "title", cfg["name"], cfg["affiliation"])
print(header)
