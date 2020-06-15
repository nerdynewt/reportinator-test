import yaml
import os
import sys

# script = str(os.path.dirname(os.path.realpath(sys.argv[0])))

configlist = ["~/.config/reportinator/config.yaml", "~/.reportinator.yaml", "/etc/reportinator.yaml", "../config/config.yaml", "config/config.yaml"]

for file in configlist:
    file=os.path.expanduser(file)
    file=os.path.abspath(file)
    if os.path.isfile(file):
        configpath=file
        configdir=os.path.dirname(file)
        break

with open (configpath, "r") as ymlfile:
    cfg=yaml.safe_load(ymlfile)


scriptlist = [cfg["install_dir"], "~/.config/reportinator/scripts", "~/.local/share/reportinator", "/usr/share/reportinator" , "../config/scripts", "../share"]
scripts=[]
for files in scriptlist:
    if files:
        files=os.path.expanduser(files)
        files=os.path.abspath(files)
        if os.path.exists(files):
            for file in os.listdir(files):
                scripts.append(files+"/"+file)


def scriptmatcher(search_term):
    scriptlist = [cfg["install_dir"], "~/.config/reportinator/scripts", "~/.local/share/reportinator", "/usr/share/reportinator" , "../config/scripts", "../share", ]
    scripts=[]
    for files in scriptlist:
        if files:
            files=os.path.expanduser(files)
            files=os.path.abspath(files)
            if os.path.exists(files):
                for file in os.listdir(files):
                    scripts.append(files+"/"+file)
    scriptmatch=""
    scriptmatch="\n".join(s for s in scripts if search_term in s).split('\n', 1)[0]
    defaultmatch="\n".join(s for s in scripts if "Default.py" in s).split('\n', 1)[0]
    if scriptmatch:
        return scriptmatch
    else:
        return defaultmatch
