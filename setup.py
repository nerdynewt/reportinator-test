import os
import sys
import fileinput
import configparse
import ruamel.yaml

pythonpath = sys.executable
configpath=configparse.configpath
yaml = ruamel.yaml.YAML() 


wd=os.getcwd()

with open(configpath) as f:
    config = yaml.load(f)

if sys.argv[1] == "--installed":
    config["cache_dir"]=sys.argv[2]
    config["install_dir"]=sys.argv[3]
    config["source_dir"]=sys.argv[4]
    config["installed"]=True
    with open(configpath, "w") as f:
        yaml.dump(config, f)
    exit()

name = input("Enter name: ")
affiliation = input("Enter affiliation: ")
style = input("Enter name of the custom class file (Leave blank for default): ")

if name:
    config["name"]=name
if affiliation:
    config["affiliation"]=affiliation
if style:
    config["style"]=style
else:
    config["style"]='double'
if not config["installed"]:
    config["cache_dir"]=wd+"/cache"
    config["install_dir"]=wd+"/share"
    config["source_dir"]=wd

config["reconfig"]=False

with open(configpath, "w") as f:
    yaml.dump(config, f)

os.system(pythonpath + " -m pip install -r requirements.txt")
# config["name"] = input("Enter Name: ")
# config["affiliation"] = input("Enter Affiliation: ")
# config["style"] = input("Enter name of the custom class file (Leave blank for default): ")

# for line in fileinput.input("config.py", inplace=True):
#     if line != "":
#         if line[:5] == "name=":
#             print('{}"{}"'.format("name=", name))
#         elif line[:12] == "affiliation=":
#             print('{}"{}"'.format("affiliation=", affiliation))
#         elif line[:6] == "style=":
#             if style != "":
#                 print('{}"{}"'.format("style=", style))
#             else:
#                 print('{}"{}"'.format("style=", "double"))
#         elif line[:9] == "reconfig=":
#             print('{}{}'.format("reconfig=", "False"))
#         else:
#             print(line)
#     else:
#         pass

exit()

# import os
# import sys


# os.system(pythonpath + " -m pip install --upgrade pip")
# os.system(pythonpath + " -m pip install pandas")
# os.system(pythonpath + " -m pip install pypandoc")
# os.system(pythonpath + " -m pip install pandoc-xnos")
# os.system(pythonpath + " -m pip install \"git+https://github.com/olivierverdier/pydflatex#egg=pydflatex\"")
# os.system(pythonpath + " -m pip install blessings")
# os.system(pythonpath + " -m pip install doi2bib")
