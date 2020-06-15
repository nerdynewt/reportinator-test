import pypandoc
import sys
import configparse
import os
# pypandoc.download_pandoc()
# pypandoc.convert_text("# Heading", 'latex', format='md')
# print(sys.path)
# print(configparse.scriptmatcher("Graphsasdf"))
# print(configparse.cfg["name"])

configlist = ["~/.config/reportinator/config.yaml", "~/.reportinator.yaml", "/etc/reportinator.yaml", "../config/config.yaml", "./config/config.yaml"]

for file in configlist:
    file=os.path.expanduser(file)
    file=os.path.abspath(file)
    if os.path.isfile(file):
        configpath=file
        configdir=os.path.dirname(file)
        break
print(configpath)
