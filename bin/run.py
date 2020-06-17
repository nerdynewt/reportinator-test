#!/bin/python3

import os
import glob,os
import argparse
import sys
import shutil
import csv
import configparse
from distutils.dir_util import copy_tree

# Defining Variables
wd = os.getcwd()
pythonpath = sys.executable

# Argparser
parser = argparse.ArgumentParser(description='Welcome to Reportinator 1.0')
parser.add_argument('--source', required=False, default=False, help="Directory path of the source files, without / at the end")
parser.add_argument('--reconfig', required=False, default=False, action="store_true", help="Run the reconfiguration script")
args = parser.parse_args()

if not args.source:
    path = wd
else:
    path = args.source


# Reading Configuration
cfg=configparse.cfg # A dictionary object containing configuration

if cfg["reconfig"] or args.reconfig:
    print("Performing reconfiguration setup...")
    os.system(pythonpath+" "+BIN_DIR+"/setup.py")
    os.system(pythonpath+" install.py")

documentstyle = cfg["style"]
cache_dir=cfg["cache_dir"]
configpath=configparse.configpath
configdir=configparse.configdir

# === end of configuration

print("Your LaTeX code is being processed. Please check your source directory")

# Copying over files
shutil.rmtree(cache_dir, ignore_errors=True, onerror=None)
os.mkdir(cache_dir)
# os.mkdir(cache_dir+'/process')
# os.mkdir(cache_dir+'/texts')
os.mkdir(cache_dir+'/csvs')

for file in os.listdir(path):
    ext=os.path.splitext(file)[1]
    if ext == '.md':
        tempath = cfg["cache_dir"]+"/"+file
        shutil.copy(path+'/'+file, cache_dir+"/"+file)
    elif ext == '.csv':
        shutil.copy(path+'/'+file, cache_dir+"/csvs/"+file)
    else:
        shutil.copy(path+'/'+file, cache_dir+"/"+file)

# Iterating Over Sections and Calling Scripts
os.system(pythonpath+" "+ configparse.scriptmatcher("Header")+ " --config " + configpath + " >> " +cache_dir+"/"+"output.tex") # Header

with open(tempath) as f:
    lines=f.readlines()

sections = list()
section=""
for line in lines:
    if line[:2] == '# ':
        sections.append(section)
        section=""
    section+=line

for section in sections[1:]:
    name=section.split('\n', 1)[0][2:]
    os.system(pythonpath+" "+ configparse.scriptmatcher(name)+ " \'" + section + "\' --config " + configpath + " >> " +cache_dir+"/"+"output.tex")

os.system(pythonpath+" "+ configparse.scriptmatcher("Footer")+ " --config " + configpath + " >> " +cache_dir+"/"+"output.tex") # Footer

# Copying files back and compiling
# shutil.copytree(cache_dir, path)
copy_tree(cache_dir, path)
# shutil.copy(cfg["cache_dir"]+"/output.tex", path+"/report.tex")
# shutil.copy(cfg["cache_dir"]+"/output.bib", path+"/output.bib")
shutil.copy(configdir+"/layouts/"+documentstyle+".cls", path+"/"+documentstyle+".cls")
os.chdir(path)
os.system("pydflatex -x -t -k -o report.tex")
# for f in glob.glob("*.aux" or "*.bcf" or "*.log" or "*.run.xml" or "*.fls" or ".fbd.latexmk" or ".blg"):
#     os.remove(f)
print("Your shit's sorted")
