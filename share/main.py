## Almost done, but don't run, no fallback options edited in
import os
import pandas as pd
import csv
import argparse
import shutil
import sys
import config

# Change working directory
script = str(os.path.dirname(os.path.realpath(sys.argv[0])))
os.chdir(script)
pythonpath = sys.executable

# Source Directory
parser = argparse.ArgumentParser(description='Welcome to Reportinator 1.0')
parser.add_argument('--source', required=True, help="Directory path of the source files, without / at the end")
args = parser.parse_args()
path = args.source

# EXTRACT FUNCTION
def extract(string, start='(', stop=')'):
    return string[string.index(start)+1:string.index(stop)]

# INCLUDE IMAGE FUNCTION
def image(source):
    with open(source, "r") as f:
        for line in f:
            content = line.strip()
            if content[:6] == "image(":
                file = content[content.index('(')+1:content.index(')')]
                os.system(pythonpath+" image.py --file "+file)    
            else:
                print (content)


# GETTING DATA
os.system(pythonpath+" separate.py --file "+path)

def ext(fp):
    ext = os.path.splitext(fp)[-1].lower()
    if ext == ".csv":
        return ("csv")
    elif ext == ".md":
        return ("md")
    else:
        return ("something")


for file in os.listdir("../"):
    path = '../'+file
    if ext(path) == "md" and file[:-3] != "README":
        inputfile = file[:-3]

# GLOBAL METADATA
documentstyle = config.style
author = config.name
affiliation = config.affiliation
title=inputfile

# MAKE FILE, CODE and CSV LISTS
source_csv = []
file_list = []
code_list = []
for file in os.listdir("../_assets/texts"):
    file_list.append(file)
file_list.sort()
for file in os.listdir("../_scripts"):
    code_list.append(file)
for file in os.listdir("../_assets/csvs"):
    source_csv.append(file)


# CODE FOR WRITING
print ("\\documentclass{"+documentstyle+"}\n")
print ("\\begin{"+"document}\n")
print ("\\title{"+title+"}\n")
print ("\\author{"+author+"\\thanks{"+affiliation+"}"+"}\n")
print ("\\date{"+"\\today"+"}")
print ("\\maketitle\n")

# FOR NUMBER OF COLUMNS
def numcol(file):
    datafilename = '../_assets/csvs/'+file
    f=open(datafilename,'r')
    reader=csv.reader(f,delimiter=',')
    ncol=len(next(reader)) 
    f.seek(0)
    for row in reader:
        pass
    return ncol

# TABLE METADATA
def table_header(n):
    i = 1
    cs = '|'
    while i < n+1:
        cs = cs+'c|'
        i+=1
    print("\\begin{"+"table"+"}[H]"+"\n"+"\\centering"+"\n"+"\\resizebox{"+"\\columnwidth"+"}{"+"!"+"}{%"+"\n"+"\\begin{"+"tabular"+"}{"+cs+"}"+"\n"+"\\hline")

def tab_foot(tab_caption, tab_label):
    table_footer = "\\end{"+"tabular"+"}%"+"\n"+"}"+"\n"+"\\caption{"+tab_caption+"}"+"\n"+"\\label{"+"tbl:\""+tab_label+"\"}"+"\n"+"\\end{"+"table"+"}"
    print (table_footer)

for file in file_list:
    ## We have the file[1:] to account for naming as 1Abc. The ordering is set by the numbering in front.
    
    # ABSTRACT
    if file[1:] == "Abstract":
        name = file[1:] 
        print ("\\begin{"+"abstract"+"}")
        f = open("../_assets/texts/"+file, 'r')
        file_contents = f.read()
        print (file_contents)
        print ("\\end{"+"abstract"+"}")

    # TABLES
    elif file[1:] == "Observations":
        name = file[1:] 
        print ("\\section{"+name+"}")
        for source in source_csv:
            if source != ".DS_Store":
                n = numcol(source)
                table_header(n)
                os.system(pythonpath+" tably.py -fec table ../_assets/csvs/" + source)   
                tab_foot(source[:-4],source[:-4])
            # figure out exactly
    elif file[1:] == "DS_Store":
        pass
    # GRAPHS
    elif file[1:] == "Graphs":
        name = file[1:] 
        print ("\\section{"+name+"}")
        n=0
        for source in source_csv:
            # read last line
            if source != ".DS_Store":
                csv_path = "../_assets/csvs/"+source
                with open (csv_path) as f:
                    data = f.readlines()
                lastline = data[-1]
                lastline = lastline.split(')')
                lastline = lastline[0]
                lastline = lastline[1:]+')'
                penline = data[-2]
                compare = lastline[:5]
                if compare == "graph":
                    graph = extract(lastline) #stuff between brackets
                    graph_list = []
                    fit_list = []
                    if penline[:5] == "\"fit(":
                        fitlist = extract(penline) #stuff between brackets
                        fit_list = fitlist.split(',')
                    graph_list = graph.split(';')
                    i = 0
                    while i < len(graph_list):
                        grlst = graph_list[i]
                        if fit_list:
                            fitfun = fit_list[i]
                            if fit_list[i] == "0":
                                fitfun == False
                            figure = pythonpath+" figures.py --file "+source+" --list "+str(grlst)+" --index "+str(n)+" --fit "+fitfun
                        else:
                            figure = pythonpath+" figures.py --file "+source+" --list "+str(grlst)+" --index "+str(n)
                        os.system(figure)
                        i+=1
                        n+=1
            
    # NEW CODE AND REST   
    else:
        name = file[1:]
        print ("\\section{"+name+"}")
        path = "../_assets/texts/"+file
        image(path)
        if (name+".py" in code_list):
            code = pythonpath+" "+name+".py"
            os.system(code)
print ("\\clearpage")
print ("\\end{document"+"}")
os.remove("../"+inputfile+".md")