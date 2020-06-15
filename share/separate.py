import os
import csv
import pandas as pd
import shutil
import argparse
import pypandoc

# Parse source
parser = argparse.ArgumentParser(description='Program for processing text and assets for reportinator 1.0')
parser.add_argument('--file', required=True, help="Input the name of the csv file to be converted into a figure, placed in assets")
args = parser.parse_args()
source = args.file

# Extension helper: https://stackoverflow.com/questions/5899497/how-can-i-check-the-extension-of-a-file
def ext(fp):
    ext = os.path.splitext(fp)[-1].lower()
    if ext == ".csv":
        return ("csv")
    elif ext == ".md":
        return ("md")
    else:
        return ("something")

# Make new directories 
for file in os.listdir("../"):
    path = '../'+file
    if ext(path) == "md" and file[:-3] != "README":
        os.remove(path)

shutil.rmtree("../_assets", ignore_errors=True, onerror=None)
os.mkdir('../_assets')
os.mkdir('../_assets/process')
os.mkdir('../_assets/texts')
os.mkdir('../_assets/csvs')

# Copy over contents 
for file in os.listdir(source):
    path = source+'/'+file
    if ext(path) == "csv":
        shutil.copy(path,'../_assets/csvs/'+file)
    elif ext(path) == "md":
        inputdir = '../'+file
        shutil.copy(path,'../'+file)
    else:
        shutil.copy(path,'../_assets/'+file)

# Separate into numbers
with open(inputdir, "r") as f:
    head = []
    k = 1
    for lane in f:
        stripped = lane.strip()
        if stripped[:2] == "# ":
            head.append(lane)     
            k += 1
   
        else:
            pass

with open(inputdir, "r") as g:
    buff = [] 
    i = 64
    for line in g:
        stripped = line.strip()
        if stripped[:2] != "# ":
            buff.append(line)
            output = open('../_assets/process/'+chr(i)+'.txt','w')
            output.write(''.join(buff))
            output.close()
        else:
            i += 1
            buff = []

i = 65
while i < len(head) + 64:
    filename = "../_assets/process/"+chr(i)+".txt"
    append_copy = open(filename, "r")
    original_text = append_copy.read()
    append_copy.close()
    append_copy = open(filename, "w")
    append_copy.write(head[i-64])
    append_copy.write(original_text)
    append_copy.close()
    i += 1

# Rename and remove
for file in os.listdir("../_assets/process"):
    with open ("../_assets/process/"+file, 'r') as f:
        num = str(file[:-4])
        data = f.read().splitlines(True)
        firstline = data[0]
        lastline = data[-1]
        title = firstline[2:-1]
        title = "../_assets/texts/"+num+title
    with open(title, 'w') as fout:
        fout.writelines(data[1:])

for file in os.listdir("../_assets/texts"):
    filters = ['pandoc-xnos']
    pdoc_args = ['--wrap=preserve']
    shutil.copy("../_assets/texts/"+file, "../_assets/texts/"+file+".md")
    output = pypandoc.convert_file("../_assets/texts/"+file+".md", to='latex', format='markdown-auto_identifiers' ,outputfile="../_assets/texts/"+file+".tex", extra_args=pdoc_args,
                         filters=filters)
    assert output == ""
    os.remove("../_assets/texts/"+file+".md")
    shutil.copy("../_assets/texts/"+file+".tex", "../_assets/texts/"+file)
    os.remove("../_assets/texts/"+file+".tex")
