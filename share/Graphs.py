import argparse
import sys
import configparse
import os
import csv

pythonpath = sys.executable
cache_dir=configparse.cfg["cache_dir"]
source_csv=[]
for file in os.listdir(cache_dir+"/csvs"):
    source_csv.append(file)

def extract(string, start='(', stop=')'):
    return string[string.index(start)+1:string.index(stop)]

section=sys.argv[1]
name=section.split('\n', 1)[0][2:]
# print(section+ '\n')

for source in source_csv:
    if source == ".DS_Store":
        continue
    csv_path=cache_dir+"/csvs/"+source
    data = list(csv.reader(open(csv_path)))
    lastline = data[-1]
    graphmatch="\n".join(s for s in lastline if "graph(" in s).split('\n', 1)[0]
    fitmatch="\n".join(s for s in lastline if "fit(" in s).split('\n', 1)[0]
    fit_list=extract(fitmatch).split(',')
    fitfun=fit_list[0]
    n=0
    for graphs in graphmatch:
        graph_list=extract(graphmatch).split(',')
        graph_list=str(graph_list).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
        if fitmatch:
            figure = pythonpath+ " " +configparse.scriptmatcher("figures.py") + " --file "+source+" --list "+graph_list+" --index "+str(n)+" --fit "+fitfun
        else:
            figure = pythonpath+ configparse.scriptmatcher("figures.py") + " --file "+source+" --list "+graph_list+" --index "+str(n)
        n=n+1
    os.system(figure)
    print(" ")
